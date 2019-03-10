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

@app.route('/signup_usuario', methods=['POST'])
def registroUsuarioPost():
    #vacio mensaje de session
    session['messages'] = ''
    # check campos vacios
    missing = []
    fields = [ 'nombre' , 'apellido', 'tipo_doc', 'nro_documento','fecha_nac', 'tel','email', 'repetir_email', 'password', 'repetir_password']
    for field in fields:
        value = request.form.get(field, None)
        if value is None:
            missing.append(field)
        #sino validar si es ci que sean solo numeros y cantidad 8 (esto lo deberia hacer un javascript antes igual)
    if missing:
        return render_template('signup_usuario.html')

    #ESTO FALTA check email - repetir_email y pass y repetir pass iguales   (esto lo deberia hacer un javascript antes igual, el pass capaz que no, solo aca , a definir)
    
    #Me fijo que no haya ningun usuario con ese email
    mycursor.execute( """
        SELECT * 
        FROM Usuario 
        WHERE email = %s
        """, [request.form.get('email')]) 
    rows = mycursor.fetchall()
    if not rows:
        #obtengo el id del ultimo insert
        mycursor.execute( """
        SELECT idUsuario 
        FROM Usuario ORDER BY idUsuario DESC LIMIT 1
        """ ) 
        rows = mycursor.fetchall()
        idUsuario = rows[0][0]
        idUsuario = idUsuario + 1
        #hago el insert en la tabla usuario
        mycursor.execute( """
        INSERT INTO Usuario (idUsuario, email, password)
        VALUES ( %s,  %s,  %s) """, { idUsuario,  [request.form.get('email')], [request.form.get('password')]}) 
        #hago el insert en la tabla cliente
        #tipo de documento no lo estoy registrando porque me falto crear esa columna, lo hago despues 
        mycursor.execute( """
        INSERT INTO Cliente (idUsuario, nombre, apellido,ci,sexo,celular,fecDeNac,ecobit)
        VALUES ( %s, %s, %s, %s, %s, %s, %s,0) 
        """, {idUsuario, [request.form.get('nombre')], [request.form.get('apellido')],  [request.form.get('nro_documento')],  [request.form.get('sexo')],  [request.form.get('tel')], [request.form.get('fecha_nac')]}) 
        rows = mycursor.fetchall()
        return render_template('ingresar.html')
    else:
        session['messages'] = 'El email ya está en uso.' #hay que ver como borrar esto porque hasata que no ande el post de nuevo, o sea se registre de verdad ok, no se va a borrar
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