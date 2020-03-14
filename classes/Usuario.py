class Usuario:
  def __init__(self, mail,password, saldo, nombre,foto):
    self.mail = mail
    self.password = password
    self.saldo = saldo
    self.nombre = nombre
    self.foto = foto

  def __dict__(self):
    return {
      "email": self.mail,
      "saldo": self.saldo,
      "nombre": self.nombre,
      "foto": self.foto
    }
