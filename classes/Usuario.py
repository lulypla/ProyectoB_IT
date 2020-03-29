class Usuario:
  def __init__(self,id, email,password,nombre,saldo , foto, apellido, tel,nro_doc,tipo_doc,fecha_nac, activo):
    self.id = id
    self.email = email
    self.password = password
    self.saldo = saldo
    self.nombre = nombre
    self.foto = foto
    self.apellido = apellido
    self.tel = tel
    self.nro_doc = nro_doc
    self.tipo_doc = tipo_doc
    self.fecha_nac = fecha_nac
    if(activo == 1):
      self.activo = True
    else:
      self.activo = False

  def __dict__(self):
    return {
      "email": self.email,
      "saldo": self.saldo,
      "nombre": self.nombre,
      "apellido": self.apellido,
      "fecha_nac": self.fecha_nac,
      "nro_doc": self.nro_doc,
      "tipo_doc": self.tipo_doc,
      "foto": self.foto,
      "tel": self.tel,
      "activo": self.activo
    }
