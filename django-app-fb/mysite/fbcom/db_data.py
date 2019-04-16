import MySQLdb as mysql

DB_NAME = "trial"

class MySQLDB():
    def __init__(self):
        self.con = mysql.connect("localhost", "root", "root", DB_NAME)

    def _prepare_exec(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        print dir(cur)
        return cur

    def get_all_data(self):
        cur = self._prepare_exec("select * from users")
        return self.serialize(cur.fetchall())

    def serialize(self, data):
        result = []
        for i in data:
            id, name, email = i
            result.append({
                "id": id,
                "name": name,
                "mail": email
            })

        return result
