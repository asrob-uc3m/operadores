import requests
import json
from tqdm import tqdm
import begin


class DataRetriever(object):
    """
    Retrieves data from github, catching the already visited urls to avoid unnecessary requests
    """
    def __init__(self, token=None):
        self.cache = {}
        if token:
            self.params = {'access_token': token}
        else:
            self.params = None

    def retrieve(self, url):
        if url not in self.cache:
            resp = requests.get(url=url, params=self.params)
            data = json.loads(resp.text)
            self.cache[url] = data

        return self.cache[url]

def extract_all_data(org_name = '', access_token = ''):
    """
    Extracts data from the requested github organization. The returned dict has the
    following format:

    organization
     |- teams
     |    |- members []
     |    |- repos []
     |- repos
     |    |- open_issues []
     |    |- issues
     |    |    |- title
     |    |    |- assignees []
     |    |    |- labels []
     |    |    |- opened_by
     |    |    |- closed_by (needs to request for events)
     |    |- contributors
     |- members
     |    |- name
     |    |- avatar_url
     |    |- total_contributions
     |    |- opened_issues
     |    |- closed_issues
     |    |- assigned_issues

    :param org_name: Name of the github organization to retrieve the data from
    :param access_token: Access token that grant access to the organization private data
    :return: a organization dict with the format described in this docstring
    """
    url_org = 'https://api.github.com/orgs/{}'
    dr = DataRetriever(access_token)
    organization = {}

    # Teams
    url_teams = url_org.format(org_name)+'/teams'
    teams_data = dr.retrieve(url_teams)

    organization['teams'] = dict()
    for team in tqdm(teams_data, desc="Retrieving teams"):
        work_group = dict()
        work_group['members'] = list()
        for member in dr.retrieve(team['members_url'].replace('{/member}', '')):
            work_group['members'].append(member['login'])
        work_group['repos'] = list()
        for repo in dr.retrieve(team['repositories_url']):
            work_group['repos'].append(repo['name'])
        organization['teams'][team['name']] = work_group

    # Repos
    url_repos = url_org.format(org_name)+'/repos'
    repos_data = dr.retrieve(url_repos)

    organization['repos'] = dict()
    for repo_data in tqdm(repos_data, desc="Retrieving repos"):
        repo = dict()
        # Retrieve issues
        repo['open_issues'] = []
        repo['issues'] = dict()
        for issue_data in dr.retrieve(repo_data['issues_url'].replace('{/number}', '')+'?state=all'):
            issue = dict()
            issue['title'] = issue_data['title']
            issue['assignees'] = [asignee['login'] for asignee in issue_data['assignees']]
            issue['labels'] = [label['name'] for label in issue_data['labels']]
            issue['opened_by'] = issue_data['user']['login']
            issue['closed'] = issue_data['state'] == 'closed'
            issue['closed_by'] = None
            if not issue['closed']:
                repo['open_issues'].append(issue_data['number'])
            else:
                for event in reversed(dr.retrieve(issue_data['events_url'].replace('{/privacy}', ''))):
                    if event['event'] == 'closed':
                        issue['closed_by'] = event['actor']['login']
                        break
            repo['issues'][issue_data['number']] = issue

        # Retrieve contributors
        repo['contributors'] = dict()
        for contrib_data in dr.retrieve(repo_data['contributors_url']):
            repo['contributors'][contrib_data['login']] = contrib_data['contributions']
        organization['repos'][repo_data['name']] = repo

    # Members
    organization['members'] = dict()
    url_members = url_org.format(org_name)+'/members'
    members_data = dr.retrieve(url_members)

    for user in members_data:
        member = dict()
        member['avatar_url'] = user['avatar_url']
        # The rest of the info about members will be computed from previous data (repos)
        # Not sure if I should pre-compute all this info or compute it just when requested
        member['total_contributions'] = 0
        member['opened_issues'] = []
        member['closed_issues'] = []
        member['assigned_issues'] = []
        organization['members'][user['login']] = member

    # Compute the rest of the info about members from previous data (repos)
    for repo_name, repo_data in organization['repos'].items():
        # Add contributions per repo to each member
        for contributor, contribs in repo_data['contributors'].items():
            try:
                organization['members'][contributor]['total_contributions'] += contribs
            except KeyError:
                pass

        # Compute issues per member and classify in open/closed
        for issue, issue_data in repo_data['issues'].items():
            try:
                organization['members'][issue_data['opened_by']]['opened_issues'].append((repo_name, issue))
                if issue_data['closed_by']:
                    organization['members'][issue_data['closed_by']]['closed_issues'].append((repo_name, issue))
            except KeyError:
                pass

            for assignee in issue_data['assignees']:
                try:
                    organization['members'][assignee]['assigned_issues'].append((repo_name, issue))
                except KeyError:
                    pass

    return organization


@begin.start(auto_convert=True)
def main(org, access_token = None):
    organization = extract_all_data(org_name=org, access_token=access_token)

    print(organization['teams'])
    for name, repo in organization['repos'].items():
        print(name, repo['open_issues'], len(repo['issues']), len(repo['contributors']))
    print(organization['members'])
