from classes import *

class Empresa(Usuario):
  def __init__(self, idUsario, email,password, nombre, rut,telefono,direccion,rubro,imagen):
    Usuario.__init__(self,  idUsario, email,password)
    self.nombre = nombre
    self.rut = rut
    self.telefono = telefono
    self.direccion = direccion
    self.rubro = rubro
    self.imagen = imagen

  def myfunc(self):
    print("Hello my name is " + self.nombre)