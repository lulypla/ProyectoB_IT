import dao.db as d
import classes.Oferta as Oferta

# 0 'codigo'
# 1 'titulo'
# 2 'descripcion'
# 3 'imagen'
# 4'precio'
def get_ofertas():
    query = "SELECT * FROM oferta"
    rows = d.db_instance.query_get(query)
    ofertas = []

    for r in rows:
        oferta = Oferta.Oferta(r[0], r[1], r[2], r[3], r[4])
        ofertas.append(oferta)
    return ofertas

def get_oferta__porId(id):
    query = "SELECT * FROM oferta WHERE id=%s" % id
    rows = d.db_instance.query_get(query)
    return rows
