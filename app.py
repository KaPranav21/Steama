from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__, static_folder='static')

DB_CONFIG = {
    'user': 'root',
    'password': '4VC8SIIO?!',
    'host': 'localhost',
    'database': 'steam_project',
}

@app.route('/')
def dashboard():
    return app.send_static_file('dashboard.html')

@app.route('/api/users')
def get_users():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username FROM users")
    users = [{'user_id': row[0], 'username': row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route('/api/user/<int:user_id>/games')
def get_user_games(user_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.name, ug.playtime_hours, ug.rating
        FROM user_games ug
        JOIN games g ON ug.appid = g.appid
        WHERE ug.user_id = %s
    """, (user_id,))
    games = [
        {"name": row[0], "playtime_hours": row[1], "rating": row[2]}
        for row in cursor.fetchall()
    ]
    cursor.close()
    conn.close()
    return jsonify(games)

if __name__ == "__main__":
    app.run(debug=True)