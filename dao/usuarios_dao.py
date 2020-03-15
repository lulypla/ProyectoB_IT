from dao import db
from classes import Usuario
from services import image


def get_usuario(email):
    query = "SELECT * FROM users WHERE email='%s'" % email
    rows = db.db_instance.query_get(query)
    usuario = None
    for u in rows:
        usuario = Usuario.Usuario(u[0], u[1], u[3], u[2], u[4])
    # 0 'email'
    # 1 'password'
    # 2 'nombre'
    # 3 'saldo'
    return usuario


def login_usuario(email, password):
    usuario = get_usuario(email)
    if usuario is None:
        return None
    if usuario.password == password:
        return usuario
    return None


def create_usuario(usuario: Usuario):
    query = "INSERT INTO users (email,password,nombre,ecobits) VALUES ('{email}','{password}','{nombre}',0)".format(
        email=usuario.email, password=usuario.password, nombre=usuario.nombre
    )
    resultado = db.db_instance.query_insert(query)
    usuario_from_db = get_usuario(usuario.email)
    return usuario_from_db


def update_usuario(usuario_actualizado: Usuario):
    query = "UPDATE users SET email='{email}'" \
            "password='{password}'" \
            "nombre='{nombre}'" \
            "WHERE email='{email}'".format(
                email=usuario_actualizado.email,
                password=usuario_actualizado.password,
                nombre=usuario_actualizado.nombre)
    resultado = db.db_instance.query_insert(query)
    return resultado


def update_foto(image_data, email):
    url = image.upload_image(image_data)
    query = "UPDATE users SET foto='{foto}' WHERE email='{email}'".format(
        email=email, foto=url)
    resultado = db.db_instance.query_insert(query)
    usuario = get_usuario(email)
    if(usuario.foto != url):
        return {'error': "Error en query"}
    return usuario.__dict__()
