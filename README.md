# Printers Operators Page

Gestión de operadores autorizados a utilizar las impresoras 3D

## ¿Cómo convertirse en operador?

El requisito para poder imprimir en BLACKY o en HIJA RESURRECTION es que tienes que ser operador. Para ello:

- Tienes que abrir una issue en este repositorio con la etiqueta "training request". Alguno de los [operadores autorizados](http://asrob.uc3m.es/index.php/Operadores) se pondrá en contacto contigo respondiendo la issue y que te enseñará a imprimir. Para ello, seguiremos la metodología Maestro-Aprendiz. Nota: para publicar issues debes tener una cuenta en GitHub; puedes abrir una fácilmente.

- Cuando hayas impreso al menos 3 piezas de forma independiente bajo la supervisión del operador responsable a tu cargo, te convertirás en uno de ellos.

- Una vez seas operador:

1. Podrás imprimir tú sólo las próximas veces.
2. Podrás formar a otros operadores si lo deseas.
3. Podrás aparecer en la [lista de operadores](http://asrob.uc3m.es/index.php/Operadores). En la cual deberás añadirte al final de la lista proporcionando tu fotografía, tu nombre y apellidos y un correo electrónico (preferiblemente el de la UC3M).

# About

Automatic generation of printer operators page based on [Jinja2](http://jinja.pocoo.org/docs/2.9/) templates and [GitHub issues](https://github.com/asrob-uc3m/operadores/issues/).

Author: [Manuel Peña](https://github.com/Siotma)

# Usage

1. Install dependencies: `pip install -r requirements.txt`.
2. Copy the `website` and `template` folder to the corresponding directory in your website server.
3. Run the generate script with the path of the index.html file to write: `python operadores.py -o path/to/website/index.html`.

You will have to schedule the execution of operadores.py in order to have an updated webpage. 

# Attributions

* [Bootstrap](http://getbootstrap.com/).
* Based on the [One Page Wonder template](http://startbootstrap.com/template-overviews/one-page-wonder/).
* [Printer Status Webpage](https://github.com/asrob-uc3m/printers-status-webpage) by [David-Estevez](https://github.com/David-Estevez)
