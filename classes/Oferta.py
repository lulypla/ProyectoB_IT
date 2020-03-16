import json.encoder

class Oferta :

    def __init__(self, codigo, titulo, descripcion, imagen, precio):
        self.codigo = codigo
        self.titulo = titulo
        self.descripcion = descripcion
        self.imagen = imagen
        self.precio = precio

    def __dict__(self):
        return {
            "codigo": self.codigo,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
            "precio": self.precio,
        }