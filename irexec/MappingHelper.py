import sqlite3, json

TABLE_NAME = "remote_mapping"

def getMappingFromDB(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT config FROM '+TABLE_NAME + " WHERE active = 1")
        data = json.loads(cursor.fetchone()[0])
    except (sqlite3.OperationalError, TypeError):
        data = {}
    cursor.close()
    return data

def loadMap(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data