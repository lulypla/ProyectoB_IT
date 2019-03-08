# -*- coding: UTF-8 -*-

import sys, os
import mysql.connector
import pymysql
from classes import *
from flask import Flask, request, render_template, url_for, session, json, redirect
import json
import datetime

app = Flask(__name__)
import mysql.connector

app.secret_key = 'AVerSiFuncionaConEstaMierda'

mydb = mysql.connector.connect(host='remotemysql.com', database='0fEBhWrqlk', user='0fEBhWrqlk', password='ecobits123')
 
mycursor = mydb.cursor()


#Esto es para usar en el list clientes
# ycursor.execute("SELECT * FROM Cliente")
#ow_headers=[x[0] for x in mycursor.description]
#ows = mycursor.fetchall()
#son_data=[]
#or result in rows:
#    #if isinstance(result, datetime.datetime):
#    #    fecha = result
#    #    fecha = datetime.strptime(fecha, "%d-%m-%Y") #fecha.strftime('%m/%d/%Y') 
#    #    print (fecha)
#    #    json_data.append(dict(zip(row_headers,fecha)))
#    #else:   
#    #   json_data.append(dict(zip(row_headers,result)))
#   print (result)#(json.dumps(json_data))

@app.route('/', methods=['GET','POST'])
def index():
    session['messages'] = ''
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

@app.route('/ingresar', methods=['GET'])
def ingresar():
    if session['messages'] and session['messages'] != '' :
        #msj =  session['messages']
        #session['messages'] = ''
        return render_template('ingresar.html')
    else:
        return render_template('ingresar.html', msj = '')   

@app.route('/ingresar', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    usuarioNoRegistrado = "Usuario no registrado"
    mycursor.execute( """
        SELECT * 
        FROM Usuario 
        WHERE email = %s
        """, [email]) 
    rows = mycursor.fetchall()
    print (rows)
    if not rows:
        session['messages'] = 'El usuario no existe.'
        return redirect(url_for('ingresar'))
    elif rows[0][2] != password: 
        session['messages'] = 'La contraseña no es válida. Intente nuevamente.'
        return redirect(url_for('ingresar'))
    else:   
        session['nombre'] = nombre =  rows[0][1]
        return render_template('ofertas.html', email  = email)

@app.route('/signup_seleccion', methods=['GET','POST'])
def registro():
    # registro 
    return render_template('signup_seleccion.html')

@app.route('/signup_usuario', methods=['GET'])
def registroUsuario():
    # registro 
    return render_template('signup_usuario.html')

@app.route('/signup_empresa', methods=['GET'])
def registroEmpresa():
    # registro 
    return render_template('signup_empresa.html')

# levanta el servidor con el método run()
if __name__ == '__main__':
    if sys.platform == 'darwin':  # puerto diferente si se ejecuta en MacOsX
        app.run(debug=True, port=8080)
    else:
        app.run(debug=True, port=98)