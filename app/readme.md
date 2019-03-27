### Como instalar

Este proyecto requiere las dependencias en requirements.txt
Para instalarlas, debera de estar dentro de un venv creado con python3 o virtual-env.
Ejecutar

- pip install -r requirements.txt

Este comando instalara todas las dependencias necesarias.

Luego de instaladas las dependencias, ejecutar

- flask run

Esto levantara el servidor en modo produccion de manera local con la siguiente direccion

- http://127.0.0.1:5000

En caso de que flask muestre un error de que no encuentra "app.py" se debera ejecutar en consola el siguiente comando.

- export FLASK_APP=server.py
