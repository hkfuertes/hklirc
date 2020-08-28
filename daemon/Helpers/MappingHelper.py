import sqlite3, json

TABLE_NAME = "remote_mapping"

def read_from_db(connection_cursor, ir):
    connection_cursor.execute('SELECT config FROM '+TABLE_NAME + " WHERE active = 1 and ir = " + str(int(ir==True)))
    return connection_cursor.fetchone()[0]

def getMappingFromDB(database_path, ir = True):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    data = json.loads(read_from_db(c, ir))
    c.close()
    return data

def loadMap(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data