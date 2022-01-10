# Bot Send Messages Whatsapp

Es un bot para enviar cierta cantidad de mensajes definidos en un csv que esta en resources/messages.csv a ciertos contactos registrados del whatsapp que se especifican en el archivo resources/contacts.csv.

### resources/messages.csv
En este archivo es necesarios 2 datos: message y quantity.

### resources/contacts.csv
En este archivo es necesario 1 dato: contact_name

>Nota: En ambos archivos es necesario que la primera fila lleve los encabezados.

Para que la aplicación funcione hay que tener el driver del navegador, en este caso se utilizó Chrome.

La instalacion del paquete de python 'chromedriver-binary' depende de la version del navegador por lo que si es necesario cambiarla por la version que tiene la computadora entonces hay que modificar el archivo requierements.txt donde estan los paquetes de instalacion.