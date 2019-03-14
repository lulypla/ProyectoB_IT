# -*- coding: UTF-8 -*-

import sys
import os
import mysql.connector
import pymysql
from classes import *
from flask import Flask, request, render_template, url_for, session, json, redirect, flash
import json
import datetime

app = Flask(__name__)

app.secret_key = 'AVerSiFuncionaConEstaMierda'

mydb = mysql.connector.connect(
    host='remotemysql.com', database='AqoOvh1tJq', user='AqoOvh1tJq', password='IWv4eTB3oe')

mycursor = mydb.cursor()


# Esto es para usar en el list clientes
# ycursor.execute("SELECT * FROM Cliente")
# ow_headers=[x[0] for x in mycursor.description]
# ows = mycursor.fetchall()
# son_data=[]
# or result in rows:
#    #if isinstance(result, datetime.datetime):
#    #    fecha = result
#    #    fecha = datetime.strptime(fecha, "%d-%m-%Y") #fecha.strftime('%m/%d/%Y')
#    #    print (fecha)
#    #    json_data.append(dict(zip(row_headers,fecha)))
#    #else:
#    #   json_data.append(dict(zip(row_headers,result)))
#   print (result)#(json.dumps(json_data))

@app.route('/', methods=['GET', 'POST'])
def index():
    session['messages'] = ''
    # el servidor arranca con esta página raiz
    return render_template('index.html')


@app.route('/ofertas', methods=['GET'])
def ofertas():
        # pagina ofertas
    mycursor.execute("""
        SELECT *
        FROM Oferta
        """)
    rows = mycursor.fetchall()
    return render_template('ofertas.html', ofertas=rows)


@app.route('/centros', methods=['GET', 'POST'])
def centros():
        # listado de comercios adheridos y centros de canje
    return render_template('centros.html')


@app.route('/EcoBits', methods=['GET', 'POST'])
def EcoBits():
        # sobre EcoBits
    return render_template('EcoBits.html')


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
        # Contacto - formulario, teléfono,...
    return render_template('contacto.html')


@app.route('/FAQ', methods=['GET', 'POST'])
def faq():
        # preguntas frecuentes
    return render_template('faq.html')


@app.route('/ingresar', methods=['GET'])
def ingresar():
    if session:
        msj = session['messages']
        return render_template('ingresar.html', msj='')
    else:
        return render_template('ingresar.html')


@app.route('/procesaLogin', methods=['POST'])
def login():
    session['messages'] = ''
    email = request.form['email']
    password = request.form['password']
    usuarioNoRegistrado = "Usuario no registrado"
    mycursor.execute("""
        SELECT *
        FROM Usuario
        WHERE email = %s
        """, [email])
    rows = mycursor.fetchall()
    if not rows:
        session['messages'] = 'El usuario no existe.'
        return render_template('ingresar.html',mensaje=session['messages'])
    elif rows[0][2] != password:
        session['messages'] = 'La contraseña no es válida. Intente nuevamente.'
        return render_template('ingresar.html',mensaje=session['messages'])
    else:
        session['email'] = rows[0][1]
        session['idUsuario'] = rows[0][0]
        return redirect(url_for('ofertas'))


@app.route('/signup_seleccion', methods=['GET', 'POST'])
def registro():
    # registro
    return render_template('signup_seleccion.html')


@app.route('/signup_usuario', methods=['GET'])
def registroUsuario():
    # registro
    return render_template('signup_usuario.html')


@app.route('/signup_usuario', methods=['POST'])
def registroUsuarioPost():
    # vacio mensaje de session
    session['messages'] = ''
    # check campos vacios
    missing = []
    fields = ['nombre', 'apellido', 'tipo_doc', 'nro_documento', 'fecha_nac',
              'tel', 'email', 'repetir_email', 'password', 'repetir_password']
    for field in fields:
        value = request.form.get(field, None)
        if value is None:
            missing.append(field)
        # sino validar si es ci que sean solo numeros y cantidad 8 (esto lo deberia hacer un javascript antes igual)
    if missing:
        return render_template('signup_usuario.html')

    # ESTO FALTA check email - repetir_email y pass y repetir pass iguales   (esto lo deberia hacer un javascript antes igual, el pass capaz que no, solo aca , a definir)

    # Me fijo que no haya ningun usuario con ese email
    mycursor.execute("""
        SELECT *
        FROM Usuario
        WHERE email = %s
        """, [request.form.get('email')])
    rows = mycursor.fetchall()
    if not rows:
        # obtengo el id del ultimo insert
        mycursor.execute("""
        SELECT idUsuario
        FROM Usuario ORDER BY idUsuario DESC LIMIT 1
        """)
        rows = mycursor.fetchall()
        idUsuario = rows[0][0]
        idUsuario = idUsuario + 1
        # hago el insert en la tabla usuario
        sql = "INSERT INTO Usuario (idUsuario, email, password, tipo) VALUES ("+str(idUsuario)+",'"+[
            request.form.get('email')][0]+"','"+[request.form.get('password')][0]+"',"+str(1)+")"
        mycursor.execute(sql)
        # hago el insert en la tabla cliente
        sql = "INSERT INTO Cliente (idUsuario, nombre, apellido,ci,sexo,celular,fecDeNac, ecobit, tipoDoc) VALUES ("+str(idUsuario)+" ,'"+[request.form.get('nombre')][0]+"' , '"+[request.form.get('apellido')][0]+"' , '" + [
            request.form.get('nro_documento')][0]+"' , '" + [request.form.get('sexo')][0]+"' , '" + [request.form.get('tel')][0]+"' , '" + str([request.form.get('fecha_nac')][0])+"' , "+str(0)+" , '"+[request.form.get('tipo_doc')][0] + "')"
        mycursor.execute(sql)
        # actualizo en la base los insert
        mydb.commit()
        return render_template('ingresar.html')
    else:
        # hay que ver como borrar esto porque hasata que no ande el post de nuevo, o sea se registre de verdad ok, no se va a borrar
        session['messages'] = 'El email ya está en uso.'
        return render_template('signup_usuario.html')


@app.route('/signup_empresa', methods=['GET'])
def registroEmpresa():
    # registro
    return render_template('signup_empresa.html')


@app.route('/update_usuario', methods=['GET'])
def updateUsuario():
    return render_template('update_usuario.html')


@app.route('/update_usuario_getDATA', methods=['GET'])
def getDataUsuario():
    # consulto tabla cliente
    idUsuario = session['idUsuario']
    email = session['email']
    mycursor.execute("""
        SELECT *
        FROM Cliente
        WHERE idUsuario = %s
        """, [idUsuario])
    rows = mycursor.fetchall()
   # idUsuario, nombre, apellido,ci,sexo,celular,fecDeNac,ecobit, tipoDoc
    data = {}
    data['nombre'] = rows[0][1]
    data['apellido'] = rows[0][2]
    data['documento'] = rows[0][3]
    data['sexo'] = rows[0][4]
    data['celular'] = rows[0][5]
    data['fechaDeNac'] = rows[0][6]
    data['tipoDoc'] = rows[0][8]
    data['email'] = email
    return json.dumps(data)


@app.route('/update_usuario', methods=['POST'])
def postUpdateUsuario():
    # vacio mensaje de session
    session['messages'] = ''
    email = session['email']
    idUsuario = session['idUsuario']
    # check campos vacios
    missing = []
    fields = ['nombre', 'apellido', 'tipo_doc', 'nro_documento', 'fecha_nac',
              'tel', 'email', 'repetir_email', 'password', 'repetir_password']
    for field in fields:
        value = request.form.get(field, None)
        if value is None:
            missing.append(field)
        # sino validar si es ci que sean solo numeros y cantidad 8 (esto lo deberia hacer un javascript antes igual)
    if missing:
        return redirect(url_for('update_usuario.html'))

    # Me fijo que haya ningun usuario con ese email
    mycursor.execute("""
        SELECT *
        FROM Usuario
        WHERE email = %s
        """, [email])
    rows = mycursor.fetchall()
    if rows:
        password = [request.form.get('password')][0]

        # hago el update en la tabla Usuario
        email = [request.form.get('email')][0]
        password = [request.form.get('password')][0]
        sql = "UPDATE Usuario set email = '"+email+"', password = '" + \
            password+"' WHERE idUsuario = "+str(idUsuario)+""
        mycursor.execute(sql)

        # hago el insert en la tabla cliente
        nombre = [request.form.get('nombre')][0]
        apellido = [request.form.get('apellido')][0]
        fechaNac = str([request.form.get('fecha_nac')][0])
        sql = "UPDATE Cliente set nombre = '"+nombre+"', apellido = '"+apellido+"' ,ci = '" + [request.form.get('nro_documento')][0]+"' ,sexo= '"+[request.form.get(
            'sexo')][0]+"',celular='"+[request.form.get('tel')][0]+"',fecDeNac= '" + fechaNac+"', tipoDoc = '" + [request.form.get('tipo_doc')][0]+"' WHERE idUsuario = "+str(idUsuario)+""
        mycursor.execute(sql)
        # actualizo en la base los insert
        mydb.commit()
        session['email'] = email
        return redirect(url_for('updateUsuario'))
    else:
        # hay que ver como borrar esto porque hasata que no ande el post de nuevo, o sea se registre de verdad ok, no se va a borrar
        session['messages'] = 'Fallo el update.'
        return redirect(url_for('updateUsuario'))


@app.route('/EliminarCuenta', methods=['GET'])
def eliminarCuenta():
    
    emailUsuarioEliminar = session['email']
    idUsuarioEliminar = session['idUsuario']
    
    #Elimina en tabla Usuario
    mycursor.execute(
        """DELETE FROM Usuario WHERE email = %s """, [emailUsuarioEliminar])
    mydb.commit()
    
    #Elimina en tabla Cliente
    mycursor.execute(
        """DELETE FROM Cliente WHERE idUsuario = %s """, [idUsuarioEliminar])
    mydb.commit()
    
    # flash('Cuenta Eliminada Satisfactoriamente')
    return cerrarSesion()


@app.route('/cerrarSesion', methods=['GET'])
def cerrarSesion():

    session.clear()
    return render_template('index.html')


# levanta el servidor con el método run()
if __name__ == '__main__':
    if sys.platform == 'darwin':  # puerto diferente si se ejecuta en MacOsX
        app.run(debug=True, port=8080)
    else:
        app.run(debug=True, port=98)
