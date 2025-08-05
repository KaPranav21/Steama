import mysql.connector

DB_CONFIG = {
    'user': 'root',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'steam_project',
}

def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            appid INT PRIMARY KEY
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_appid(appid):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT IGNORE INTO games (appid) VALUES (%s)
    ''', (appid,))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_appids():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT appid FROM games")
    appids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return appids
