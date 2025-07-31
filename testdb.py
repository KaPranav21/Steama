import sqlite3

conn = sqlite3.connect('steam.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM games")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
