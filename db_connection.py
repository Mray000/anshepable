import sqlite3

class DbConnection:
    def __init__(self, databasename):
        self.databasename = databasename
        try:
            self.con = sqlite3.connect(self.databasename)
        except Exception as e:
            print(e)
    
    def random_text(self, type):
        cur = self.con.cursor()
        data = cur.execute("""SELECT text FROM texts
                                WHERE type = ?
                                ORDER BY RANDOM()
                                LIMIT 1""", (type, )).fetchall()
        self.con.commit()
        return data[0][0]


    def close(self):
        self.con.close()
        