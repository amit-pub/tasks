import MySQLdb as mdb
import sys
from pprint import pprint as pp

import pdb

def debug():
    pdb.set_trace()

con = mdb.connect('localhost', 'root', 'root', 'trial')

cur = con.cursor()

cur.execute("select * from users")
l = cur.fetchall()
li = list(l)

result = []
for i in li:
    r = {}
    id, name, email = i
    result.append({
        "id": id,
        "name": name,
        "mail": email
    })

pp(result)
