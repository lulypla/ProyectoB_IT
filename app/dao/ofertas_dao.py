import dao.db as d


# 0 'codigo'
# 1 'titulo'
# 2 'descripcion'
# 3 'imagen'
# 4'precio'
def get_ofertas():
    query = "SELECT * FROM oferta"
    rows = d.db_instance.query_get(query)
    return rows

def get_oferta__porId(id):
    query = "SELECT * FROM oferta WHERE id=%s" % id
    rows = d.db_instance.query_get(query)
    return rows
