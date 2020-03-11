from dao import db
from classes import Usuario


def get_usuario(mail):
    query = "SELECT * FROM users WHERE mail='%s'" % mail
    rows = db.db_instance.query_get(query)
    usuario = None
    for u in rows:
        usuario = Usuario.Usuario(u[0], u[1], u[3], u[2])
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
    query = "INSERT INTO users (mail,password,nombre,ecobits) VALUES ('{email}','{password}','{nombre}',0)".format(
        email=usuario.email, password=usuario.password, nombre=usuario.nombre
    )
    resultado = db.db_instance.query_insert(query)
    return resultado

