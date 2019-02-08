# Printers Operators Page

Gestión de operadores autorizados a utilizar las impresoras 3D. Más información [en la web](http://wiki.asrob.uc3m.es/printers/operators.html)

3D Printers authorized operators management. More info [here](http://wiki.asrob.uc3m.es/printers/operators.html)

# About

Automatic generation of printer operators page based on [Jinja2](http://jinja.pocoo.org/docs/2.9/) templates and [GitHub issues](https://github.com/asrob-uc3m/operadores/issues/).

Author: [Manuel Peña](https://github.com/Siotma)

Demo [here](http://wiki.asrob.uc3m.es/printers/operators.html)

# Usage

1. Install dependencies: `pip install -r requirements.txt`.
2. Copy the `website` and `template` folder to the corresponding directory in your website server.
3. Run the generate script with the path of the index.html file to write: `python operadores.py -o path/to/website/index.html`.

You will have to schedule the execution of operadores.py in order to have an updated webpage. 

# Attributions

* [Bootstrap](http://getbootstrap.com/).
* Based on the [One Page Wonder template](http://startbootstrap.com/template-overviews/one-page-wonder/).
* [Printer Status Webpage](https://github.com/asrob-uc3m/printers-status-webpage) by [David-Estevez](https://github.com/David-Estevez)
