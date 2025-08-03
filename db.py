import mysql.connector

DB_CONFIG = {
    'user': 'root',
    'password': '4VC8SIIO?!',
    'host': 'localhost',
    'database': 'steam_project',
}

def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            appid INT PRIMARY KEY,
            name VARCHAR(255),
            developer VARCHAR(255),
            release_date VARCHAR(50),
            type VARCHAR(100)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_game(appid, name, developer, release_date, type_):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT IGNORE INTO games (appid, name, developer, release_date, type)
        VALUES (%s, %s, %s, %s, %s)
    ''', (appid, name, developer, release_date, type_))
    conn.commit()
    cursor.close()
    conn.close()
