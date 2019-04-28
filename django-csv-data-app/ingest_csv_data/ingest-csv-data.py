import csv
import sys

import MySQLdb

data = []

filename = "sample_data.csv"
USERNAME = "root"
PASSWORD = "root"
DB_HOST = "localhost"
DB_NAME = "csvdata"
TABLE_NAME = "csvdata"
TABLE_NAME = "testdata"

COL_DATATYPE_MAP = {
    "revenue":  
'revenue', 'installs', 'country', 'spend', 'date', 'impressions', 'os', 'clicks', 'channel'
}


def read_data(filename):
    with open(filename, mode="r") as infile:
        reader = csv.reader(infile)
        columns = reader.next()
        # create dict keys by reading first
        for rows in reader:
            temp = {}
            #values = rows.split()
            for index, col in enumerate(columns):
                temp[col] = rows[index]
            data.append(temp)


def get_db_conn():
    return MySQLdb.connect(host=DB_HOST, user=USERNAME,
                           passwd=PASSWORD, db=DB_NAME)
    
def create_table(conn):
    cur = conn.cursor()
    cur.execute("create table %s ")

def ingest_data(fname):
    conn = get_db_conn()
    create_table(conn)
    cur = conn.cursor()
    cur.execute("select * from %s" % TABLE_NAME)
    print cur.fetchall()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        fname = filename
    print "'%s' file is getting processed....." % fname
    read_data(fname)
    print "'%d' rows are added" % len(data)
    import pdb; pdb.set_trace()
    #ingest_data(fname)
