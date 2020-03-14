class Usuario:
  def __init__(self, email,password, saldo, nombre,foto):
    self.email = email
    self.password = password
    self.saldo = saldo
    self.nombre = nombre
    self.foto = foto

  def __dict__(self):
    return {
      "email": self.email,
      "saldo": self.saldo,
      "nombre": self.nombre,
      "foto": self.foto
    }
