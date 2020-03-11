class Usuario:
  def __init__(self, email,password, saldo, nombre):
    self.email = email
    self.password = password
    self.saldo = saldo
    self.nombre = nombre

  def __dict__(self):
    return {
      "email": self.email,
      "saldo": self.saldo,
      "nombre": self.nombre
    }

  def myfunc(self):
    print("Hello my name is " + self.email)