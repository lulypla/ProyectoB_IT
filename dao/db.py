import mysql.connector

host = 'remotemysql.com'
user = 'QGOUX74uPC'
database='QGOUX74uPC'
password = 'VWElHacgyS'

class db:

    def __init__(self):
        self.con = mysql.connector.connect(host=host, database=database, user=user, password=password, connect_timeout=50000)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()

    def connect(self):
        self.con = mysql.connector.connect(host=host, database=database, user=user, password=password,
                                           connect_timeout=50000)
        self.cur = self.con.cursor()
    def query_get(self, text):
        try:
            self.cur.execute(text)
        except (mysql.connector.errors.InterfaceError):
            self.connect()
            self.cur.execute(text)
        rows = self.cur.fetchall()
        return rows

    def query_insert(self, text):
        try:
            self.cur.execute(text)
        except (mysql.connector.errors.InterfaceError):
            self.connect()
            self.cur.execute(text)
        return self.con.commit()


db_instance = db()
