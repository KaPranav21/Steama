import requests
import time
import os
import random
import mysql.connector
from dotenv import load_dotenv

# Load API key and DB password from .env
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
DB_PASS = os.getenv("DB_PASSWORD")

DB_CONFIG = {
    'user': 'root',
    'password': DB_PASS,
    'host': 'localhost',
    'database': 'steam_project',
}

def get_all_appids():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT appid FROM games")
    appids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return appids

def insert_user(user_id, username):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO users (user_id, username) VALUES (%s, %s)
    """, (user_id, username))
    conn.commit()
    cursor.close()
    conn.close()

def insert_user_game(user_id, appid, playtime):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_games (user_id, appid, playtime_hours)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE playtime_hours=VALUES(playtime_hours)
    """, (user_id, appid, playtime))
    conn.commit()
    cursor.close()
    conn.close()

def simulate_users(num_users=35, min_games=1, max_games=56):
    print(f"DB password is: {DB_PASS}")
    appids = get_all_appids()

    for user_id in range(1, num_users + 1):
        username = f"user_{user_id}"
        insert_user(user_id, username)

        # Choose a random number of games for this user
        num_games = random.randint(min_games, max_games)
        owned_games = random.sample(appids, min(num_games, len(appids)))

        for appid in owned_games:
            playtime = random.randint(10, 5000)  # minutes played
            insert_user_game(user_id, appid, playtime)

        print(f"Simulated data for {username} with {len(owned_games)} games.")
if __name__ == "__main__":
    simulate_users()