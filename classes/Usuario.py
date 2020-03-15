class Usuario:
  def __init__(self, email,password, saldo, nombre, foto, apellido, celular):
    self.email = email
    self.password = password
    self.saldo = saldo
    self.nombre = nombre
    self.foto = foto
    self.apellido = apellido
    self.celular = celular


  def __dict__(self):
    return {
      "email": self.email,
      "saldo": self.saldo,
      "nombre": self.nombre,
      "foto": self.foto,
      "apellido": self.apellido,
      "celular": self.celular,
    }
