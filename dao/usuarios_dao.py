from dao import db
from classes import Usuario
from services import image

def get_usuario(mail):
    query = "SELECT * FROM users WHERE mail='%s'" % mail
    rows = db.db_instance.query_get(query)
    usuario = None
    for u in rows:
        usuario = Usuario.Usuario(u[0], u[1], u[3], u[2], u[4])
    # 0 'mail'
    # 1 'password'
    # 2 'nombre'
    # 3 'saldo'
    return usuario


def login_usuario(mail,password):
    usuario = get_usuario(mail)
    if usuario is None:
        return None
    if usuario.password == password:
        return usuario
    return None


def create_usuario(usuario: Usuario):
    query = "INSERT INTO users (mail,password,nombre,ecobits) VALUES ('{mail}','{password}','{nombre}',0)".format(
        email=usuario.mail, password=usuario.password, nombre=usuario.nombre
    )
    resultado = db.db_instance.query_insert(query)
    return resultado

def update_usuario(usuario_actualizado: Usuario):
    query = "UPDATE users SET mail='{mail}'" \
            "password='{password}'" \
            "nombre='{nombre}'" \
            "WHERE mail='{mail}'".format(
                email=usuario_actualizado.mail,
                password=usuario_actualizado.password,
                nombre=usuario_actualizado.nombre)
    resultado = db.db_instance.query_insert(query);
    return resultado

def update_foto(image_data, mail):
    url = image.upload_image(image_data)
    query = "UPDATE users SET foto='{foto}' WHERE mail='{mail}'".format(mail=mail, foto=url)
    resultado = db.db_instance.query_insert(query);
    usuario = get_usuario(mail)
    if(usuario.foto != url):
        return {'error': "Error en query"}
    return usuario.__dict__()