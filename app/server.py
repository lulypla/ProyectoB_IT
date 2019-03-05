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
      return render_template('ingresar.html')

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
        return render_template('registro.html',email = email)
    elif rows[0][2] != password: 
        return redirect(url_for('ingresar'))
    else:    
        return render_template('ofertas.html', email  = email)
   #Esto lo deje por si queremos usuar lo de las sesiones
    #session['user_name'] = data['user_name']
    #session['messages'] = data['messages']
    #session['password'] = passwd
    #session['email'] = email
    #session['friends'] = data['friends']
    
    # nombre = request.form['nombre']
    # apellido = request.form['apellido']
    # session['nombre'] = nombre
    # session['apellido'] = apellido
    #return  return render_template('ofertas.html', request.for['name'])


@app.route('/registro', methods=['GET','POST'])
def registro():
    # registro 
    return render_template('registro.html')


# levanta el servidor con el método run()
if __name__ == '__main__':
    if sys.platform == 'darwin':  # puerto diferente si se ejecuta en MacOsX
        app.run(debug=True, port=8080)
    else:
        app.run(debug=True, port=98)