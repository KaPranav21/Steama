import sqlite3

DB_NAME = "steam.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                appid INTEGER PRIMARY KEY,
                name TEXT,
                developer TEXT,
                release_date TEXT,
                type TEXT
            )
        ''')
        conn.commit()

def insert_game(appid, name, developer, release_date, type_):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO games (appid, name, developer, release_date, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (appid, name, developer, release_date, type_))
        conn.commit()
