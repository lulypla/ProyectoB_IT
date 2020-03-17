from dao import db
from classes import Usuario
from services import image


def get_usuario(email):
    query = "SELECT * FROM users WHERE email='%s'" % email
    rows = db.db_instance.query_get(query)
    usuario = None
    for u in rows:
        usuario = Usuario.Usuario(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8], u[9], u[10])
    # 0 'id'
    # 1 "email"
    # 2 'password'
    # 3 'nombre'
    # 4 'saldo'
    # 5 'foto'
    # 6 'apellido'
    # 7 tel
    # 8 nro doc
    # 9 tipo doc
    # 10 fecha_nac
    return usuario


def login_usuario(email, password):
    usuario = get_usuario(email)
    if usuario is None:
        return None
    if usuario.password == password:
        usuario.password = None
        return usuario
    return None


def create_usuario(usuario: Usuario):
    query = "INSERT INTO users (email,password,nombre,saldo, apellido, tel,nro_doc,tipo_doc,fecha_nac) " \
            "VALUES ('{email}','{password}','{nombre}',0,'{apellido}','{tel}','{nro_doc}','{tipo_doc}','{fecha_nac}')".format(
        email=usuario.email, password=usuario.password,
        nombre=usuario.nombre,apellido=usuario.apellido,tel=usuario.tel,
        nro_doc=usuario.nro_doc,tipo_doc=usuario.tipo_doc,fecha_nac=usuario.fecha_nac
    )
    db.db_instance.query_insert(query)
    usuario_from_db = get_usuario(usuario.email)
    if(usuario_from_db is not None):
        return usuario_from_db.__dict__()
    return {'error': 'Error en el registro'}


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
