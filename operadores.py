import os
import json
from time import gmtime, strftime
import logging

import begin
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape


@begin.start(auto_convert=True)
@begin.logging
def start(output_file: 'Select website directory to write index.html'=os.path.join(os.path.split(__file__)[0],'website', 'index.html')):
    #### Get current time
    time_string_github_style=str(gmtime().tm_year-1)+(strftime("-%m-%dT%H:%M:%SZ", gmtime()))
    #logging.debug(time_string_github_style)
    
    ### This parts get the data from GitHub

    ## Generate a dict of all issues
    closed_issues_dict = dict()

    general_url="https://api.github.com/repos/asrob-uc3m/operadores/issues{}"
    retrieve_all_condition="?state=all"

    logging.debug(general_url.format(retrieve_all_condition))
        
    response = requests.get(general_url.format(retrieve_all_condition))
    all_issues_obj=json.loads(response.text)

    ## Get total number of issues
    total_n_of_issues=all_issues_obj[0]['number']
    
    ## Generate the dict
    for issue_number in range(1, total_n_of_issues+1):
        try:
            response = requests.get(general_url.format("/" + str(issue_number)))
            #logging.debug(general_url.format("/" + str(issue_number)))
            issue_obj=json.loads(response.text)
            logging.info(issue_number)
            issue=dict()
            issue['state'] = issue_obj['state']
            if issue['state'] == "open":
                logging.info("____is open")
                continue
        
            issue['created_by'] = issue_obj['user']
            issue['created_at'] = issue_obj['created_at']
            issue['closed_by'] = issue_obj['closed_by']
            issue['closed_at'] = issue_obj['closed_at']
            issue['labels'] = issue_obj['labels']
            issue['assignee'] = issue_obj['assignee']
            issue['assignees'] = issue_obj['assignees']
            issue['issue_url'] = issue_obj['url']

            closed_issues_dict[issue_number] = issue

        except KeyError:
            logging.info(issue_number)
            logging.info("____is error")
            pass

    sorted_closed_issues = sorted(closed_issues_dict.items(), key=lambda x: x[1]['closed_at'], reverse=False)

    unsorted_operators = dict()
    
    ### Generate a dict of operators
    ## Operator with login asrobuc3m is always authorized

    operator=dict()
    operator['raw_formed_date'] = "2011-06-03T09:00:00Z" # Arrival of MADRE
    operator['formed_in_issue_url'] = "http://www.reprap.org/wiki/Clone_Wars:_historia/es"
    operator['username'] = "asrobuc3m"
    operator['img_url'] = "http://asrob.uc3m.es/images/thumb/3/33/Logo_oficial.png/225px-Logo_oficial.png"
    operator['n_of_operators_formed'] = 0
    operator['authorized'] = 1 #Always
    operator['msg'] = "User with login asrobuc3m is always authorized"
    unsorted_operators[operator['username']] = operator
    
    ## Retrieve the list of operators from the issues, getting the latest update for each one
    for issue, issue_data in sorted_closed_issues:
        logging.info("Issue #" + str(issue) + " closed at " + issue_data['closed_at'])
        
        # only compute closed issues
        if issue_data['state'] == "open":
            logging.info("____is open")
            continue

        # only compute correctly labeled issues
        continue_flag = 1
        for label in issue_data['labels']:
            #logging.debug(label)
            if label['name'] == "training request":
                continue_flag=0
            if label['name'] == "renewal request":
                continue_flag=0
        if continue_flag == 1:
            continue

        try:
            # Don't update if this operator has error
            if unsorted_operators[issue_data['created_by']['login']]['authorized'] == -1:
                continue
        except KeyError:
            # First appearance for this operator
            pass
        
        # collect data 
        operator=dict()
        operator['raw_formed_date'] = issue_data['closed_at']
        operator['username'] = issue_data['created_by']['login']
        operator['img_url'] = issue_data['created_by']['avatar_url']
        operator['n_of_operators_formed'] = 0
        operator['formed_in_issue_url'] = issue_data['issue_url']
        operator['msg'] = "No message"
        
        # If trainer is in the operator list
        try:
            # If trainer doesn't have error
            if unsorted_operators[issue_data['closed_by']['login']]['authorized'] != -1:
                # If new_operator(formed_date) > trainer(formed_date)
                if operator['raw_formed_date'] > unsorted_operators[issue_data['closed_by']['login']]['raw_formed_date']:
                    unsorted_operators[issue_data['closed_by']['login']]['n_of_operators_formed'] += 1 
                    # If new_operator(formed_date) nearest than one year
                    if operator['raw_formed_date'] > time_string_github_style:
                        operator['authorized'] = 1
                    else:
                        operator['authorized'] = 0
                else:
                    operator['msg'] = "El formador de este operador no era operador en el momento de la formacion, aunque si lo fuera mas tarde"
                    operator['authorized'] = -1
            else:
                # inherits the error
                operator['msg'] = "El formador de este operador presenta errores"
                operator['authorized'] = -1
        except KeyError:
            # It is impossible to be a operator if the trainer isn't it
            operator['msg'] = "No hay constancia de que el formador de este operador sea o haya sido operador"
            operator['authorized'] = -1
            pass
            

        # add operator to the dict       
        unsorted_operators[issue_data['created_by']['login']] = operator

    ##Put the operators in order
    sorted_operators = sorted(unsorted_operators.items(), key=lambda x: x[1]['raw_formed_date'], reverse=True)

    ###Put the operators data in the required format
    sorted_auth_operators = []
    sorted_old_operators = []
    sorted_err_operators = []
    
    for operator, operator_data in sorted_operators:
        if operator_data['authorized'] == 1:
        # Make the authorized operators list
            sorted_auth_operators.append({'date':operator_data['raw_formed_date'],
            'issue_url':operator_data['formed_in_issue_url'],
            'msg':operator_data['msg'],
            'username':operator_data['username'],
            'img_url':operator_data['img_url'],
            'formed':operator_data['n_of_operators_formed']})
        elif operator_data['authorized'] == 0:
        # Make the old operators list
            sorted_old_operators.append({'date':operator_data['raw_formed_date'],
            'msg':operator_data['msg'],
            'issue_url':operator_data['formed_in_issue_url'],
            'username':operator_data['username'],
            'img_url':operator_data['img_url'],
            'formed':operator_data['n_of_operators_formed']})
        else:
        # Make the errors list
            sorted_err_operators.append({'date':operator_data['raw_formed_date'],
            'msg':operator_data['msg'],
            'issue_url':operator_data['formed_in_issue_url'],
            'username':operator_data['username'],
            'img_url':operator_data['img_url'],
            'formed':operator_data['n_of_operators_formed']})

    ### Generate the website using the template
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.split(__file__)[0],'templates')),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('index.html')
    html = template.render(auths=sorted_auth_operators,
                           olds=sorted_old_operators,
                           errs=sorted_err_operators)

    ## Only thing left is to save the rendered template
    with open(output_file, 'w') as f:
        f.write(html)
