class Usuario:
  def __init__(self, idUsario, email,password):
    self.idUsuario = idUsuario
    self.email = email
    self.password = password

  def myfunc(self):
    print("Hello my name is " + self.email)