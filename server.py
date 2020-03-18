# -*- coding: UTF-8 -*-

import sys
from dao import ofertas_dao, usuarios_dao
from flask import Flask, request, render_template, url_for, session, json, redirect, flash, jsonify
import json
from random import choice
from classes.Usuario import Usuario

app = Flask(__name__)

app.secret_key = 'secretKey'


@app.route('/', methods=['GET', 'POST'])
def index():
    session['messages'] = ''
    # el servidor arranca con esta página raiz
    return render_template('index.html')


@app.route('/ofertas', methods=['GET'])
def ofertas():
        # pagina ofertas
    rows = ofertas_dao.get_ofertas()
    return render_template('ofertas.html', ofertas=rows)

@app.route('/api/v1/ofertas', methods=['GET'])
def api_ofertas():
    ofertas = ofertas_dao.get_ofertas()
    if(ofertas is not None):
        respuesta = []
        for o in ofertas:
            respuesta.append(o.__dict__())
        return jsonify(respuesta)
    return jsonify({'error': "Error obteniendo ofertas"})



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
def saberMas():
        # a Sobre EcoBits
    return redirect(url_for('EcoBits'))


@app.route('/ingresar', methods=['GET'])
def ingresar():
    if session:
        msj = session['messages']
        return render_template('ingresar.html', msj='')
    else:
        return render_template('ingresar.html')


@app.route('/Canjear', methods=['POST', 'GET'])
def canjear():
    # VARIABLES DE GENERADOR DE CODIGO
    longitud = 5
    valores = "0123456789abcdefghijklmnopqrstwxyzABCDEFGHIJKLMNOPQRSTWXYZ"
    codigo = ''
    # RECEPCION DE JSON
    content = request.get_json()
    id = content['idOferta']
   # CONSULTA DE OFERTA ELEGIDA
    rows = ofertas_dao.get_oferta__porId(id)
    data = {}
    data['id'] = rows[0][0]
    data['titulo'] = rows[0][2]
    data['descripcion'] = rows[0][3]
    data['costo'] = rows[0][4]
    data['imagen'] = rows[0][6]
    costo = data['costo']
    # CONSULTA DE SALDO DE USUARIO SESIONADO
    idUsuario = session['idUsuario']
    usuario = usuarios_dao.get_usuario(idUsuario)
    saldo = usuario.saldo
    # EVALUACION DE CANJE
    if costo <= saldo:
        codigo = codigo.join([choice(valores) for i in range(longitud)])
        resultado = "Felicitaciones ha realizado el canje exitosamente, presentando el siguiente codigo: ", codigo, " ante el comercio podra retirar su producto. Esperamos que continue reciclando!!!"

    else:
        resultado = "Usted tiene saldo insuficiente para realizar este canje, lo invitamos a continuar reciclando!!!"
    # PREPARACION DE JSON PARA RESULT DE SUCCESS
    dataR = {}
    dataR['resultado'] = resultado
    return json.dumps(dataR)

# -----------------------------------------------


@app.route('/procesaLogin', methods=['POST'])
def login():
   #session['messages'] = ''
    email = request.form['email']
    password = request.form['password']
    #usuarioNoRegistrado = "Usuario no registrado"

    usuario = usuarios_dao.login_usuario(email, password)
    if not usuario:
        #session['messages'] = 'El usuario no existe.'
        flash("El usuario no existe")
        return render_template('ingresar.html')
        # session['messages'] = 'La contraseña no es válida. Intente nuevamente.'
        # flash("La contraseña no es válida. Intente nuevamente")
        # return render_template('ingresar.html')
    else:
        session['email'] = usuario.email
        session['idUsuario'] = usuario.email
        return redirect(url_for('ofertas'))


@app.route('/api/v1/login', methods=['POST'])
def login_api():
    data = request.get_json()
    email = data['email']
    password = data['password']
    usuario = usuarios_dao.login_usuario(email, password)
    if usuario is None:
        return jsonify({"error": "Usuario no existe o credenciales incorrectas"})
    return jsonify(usuario.__dict__())


@app.route('/api/v1/user/updatePhoto', methods=['POST'])
def upload_photo():
    data = request.get_json()
    image_data = data['image']
    mail = data['email']
    resultado = usuarios_dao.update_foto(image_data, mail)
    return jsonify(resultado)


@app.route('/usuario', methods=['GET', 'POST'])
def miPanel():
    # registro
    return render_template('usuario.html')


@app.route('/signup_usuario', methods=['GET'])
def registroUsuario():
    # registro
    return render_template('signup_usuario.html')


@app.route('/signup_usuario', methods=['POST'])
def registroUsuarioPost():
    # vacio mensaje de session
    #session['messages'] = ''
    # check campos vacios
    missing = []
    fields = ['nombre', 'apellido', 'tipo_doc', 'nro_documento', 'fecha_nac',
              'tel', 'email', 'repetir_email', 'password', 'repetir_password']
    for field in fields:
        value = request.form.get(field, None)
        if value is None:
            missing.append(field)
    if missing:
        return render_template('signup_usuario.html')

    # Me fijo que no haya ningun usuario con ese email

    rows = usuarios_dao.get_usuario(request.form.get('email'))
    if not rows:
        # hago el insert en la tabla usuario
        email = request.form.get('email')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        usuarioClase = Usuario(email, password, 0, nombre)
        usuarios_dao.create_usuario(usuarioClase)
        return render_template('ingresar.html')
    else:
        # hay que ver como borrar esto porque hasata que no ande el post de nuevo, o sea se registre de verdad ok, no se va a borrar
        #session['messages'] = 'El email ya está en uso.'
        flash('El email ya está en uso')
        return render_template('signup_usuario.html')


@app.route('/api/v1/registro', methods=['POST'])
def api_registro():
    data = request.get_json()
    email = data['email']
    password = data['password']
    nombre = data['nombre']
    apellido = data['apellido']
    tel = data.get('tel', "")
    nro_doc = data.get('nro_doc', 0)
    tipo_doc = data.get('tipo_doc', "")
    fecha_nac = data.get('fecha_nac', "")
    usuario = Usuario(None, email, password, 0, nombre, None, apellido, tel, nro_doc,tipo_doc,fecha_nac)
    usuarioResultado = usuarios_dao.create_usuario(usuario)
    return jsonify(usuarioResultado)



@app.route('/signup_empresa', methods=['GET'])
def registroEmpresa():
    # registro
    return render_template('signup_empresa.html')


@app.route('/update_usuario', methods=['GET'])
def updateUsuario():
    return render_template('update_usuario.html')


@app.route('/update_usuario_getDATA', methods=['GET'])
def getDataUsuario():
    has_id = session.get('idUsuario')
    has_email = session.get('email')
    if(has_id is None or has_email is None):
        return '', 204
    idUsuario = session['idUsuario']
    usuario = usuarios_dao.get_usuario(idUsuario)
    data = {}
    data['nombre'] = usuario.nombre
    data['apellido'] = usuario.apellido
    data['documento'] = ""
    data['sexo'] = ""
    data['tel'] = usuario.tel
    data['fechaDeNac'] = ""
    data['tipoDoc'] = ""
    data['email'] = usuario.email
    data['ecobit'] = usuario.saldo
    return json.dumps(data)


@app.route('/update_usuario', methods=['POST'])
def postUpdateUsuario():
    # vacio mensaje de session
    #session['messages'] = ''
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

    rows = usuarios_dao.get_usuario(email)
    if rows:
        password = [request.form.get('password')][0]

        # hago el update en la tabla Usuario
        email = [request.form.get('email')][0]
        password = [request.form.get('password')][0]
        sql = "UPDATE Usuario set email = '"+email+"', password = '" + \
            password+"' WHERE idUsuario = "+str(idUsuario)+""
        # mycursor.execute(sql)

        # hago el insert en la tabla cliente
        nombre = [request.form.get('nombre')][0]
        apellido = [request.form.get('apellido')][0]
        fechaNac = str([request.form.get('fecha_nac')][0])
        # sql = "UPDATE Cliente set nombre = '"+nombre+"', apellido = '"+apellido+"' ,ci = '" + [request.form.get('nro_documento')][0]+"' ,sexo= '"+[request.form.get(
        #     'sexo')][0]+"',celular='"+[request.form.get('tel')][0]+"',fecDeNac= '" + fechaNac+"', tipoDoc = '" + [request.form.get('tipo_doc')][0]+"' WHERE idUsuario = "+str(idUsuario)+""
        # mycursor.execute(sql)
        # actualizo en la base los insert
        # mydb.commit()
        session['email'] = email
        return redirect(url_for('updateUsuario'))
    else:
        # hay que ver como borrar esto porque hasata que no ande el post de nuevo, o sea se registre de verdad ok, no se va a borrar
        session['messages'] = 'Fallo el update.'
        return redirect(url_for('updateUsuario'))


@app.route('/EliminarCuenta', methods=['GET'])
def eliminarCuenta():

    emailUsuarioEliminar = session['email']

    flash("Cuenta Eliminada Satisfactoriamente")
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
