from classes import *

class Cliente(Usuario):
  def __init__(self, idUsario, email,password, nombre, apellido,ci,departamento,direccion,sexo,celular,fecDeNac,ecobit):
    Usuario.__init__(self,  idUsario, email,password)
    self.nombre = nombre
    self.apellido = apellido
    self.ci = ci
    self.departamento = departamento
    self.sexo = sexo
    self.celular = celular
    self.fecDeNac = fecDeNac
    self.ecobit = ecobit
    pass

  def myfunc(self):
    print("Hello my name is " + self.nombre)