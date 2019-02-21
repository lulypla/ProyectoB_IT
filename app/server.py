# -*- coding: UTF-8 -*-

import sys, os

from flask import Flask, request, render_template, url_for, session, json, redirect

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
	# el servidor arranca con esta página raiz
    return app.send_static_file('index.html')


# levanta el servidor con el método run()
if __name__ == '__main__':
    if sys.platform == 'darwin':  # puerto diferente si se ejecuta en MacOsX
        app.run(debug=True, port=8080)
    else:
        app.run(debug=True, port=98)