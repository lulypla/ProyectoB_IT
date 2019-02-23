# -*- coding: UTF-8 -*-

import sys, os

from flask import Flask, request, render_template, url_for, session, json, redirect

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
	# el servidor arranca con esta página raiz
    return render_template('index.html')


@app.route('/ofertas', methods=['GET','POST'])
def ofertas():
	# pagina ofertas
    return render_template('ofertas.html')

@app.route('/centros', methods=['GET','POST'])
def centros():
	# listado de comercios adheridos y centros de canje 
    return render_template('centros.html')

@app.route('/EcoBits', methods=['GET','POST'])
def EcoBits():
	# sobre EcoBits 
    return render_template('EcoBits.html')

@app.route('/contacto', methods=['GET','POST'])
def contacto():
	# Contacto - formulario, teléfono,...
    return render_template('contacto.html')

@app.route('/FAQ', methods=['GET','POST'])
def faq():
	# preguntas frecuentes 
    return render_template('faq.html')




# levanta el servidor con el método run()
if __name__ == '__main__':
    if sys.platform == 'darwin':  # puerto diferente si se ejecuta en MacOsX
        app.run(debug=True, port=8080)
    else:
        app.run(debug=True, port=98)