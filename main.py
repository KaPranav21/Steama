import requests
import time
import os
import mysql.connector
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
db_pass = os.getenv("DB_PASSWORD")

DB_CONFIG = {
    'user': 'root',
    'password': db_pass,
    'host': 'localhost',
    'database': 'steam_project',
}

PROCESSED_FILE = "pi.txt"


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


def fetch_all_apps():
    response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    response.raise_for_status()
    data = response.json()
    return data['applist']['apps']


def insert_appid(appid):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT IGNORE INTO games (appid) VALUES (%s)
    ''', (appid,))
    conn.commit()
    cursor.close()
    conn.close()


def load_processed_ids():
    if not os.path.exists(PROCESSED_FILE):
        return set()
    with open(PROCESSED_FILE, "r") as f:
        return set(int(line.strip()) for line in f if line.strip().isdigit())


def save_processed_id(appid):
    with open(PROCESSED_FILE, "a") as f:
        f.write(f"{appid}\n")


def main():
    print(f"Using DB password: {db_pass}")
    init_db()
    processed_ids = load_processed_ids()
    apps = fetch_all_apps()
    print(f"Total apps fetched: {len(apps)}")

    count = 0
    for app in apps[:100]:  # limit for demo
        appid = app['appid']
        if appid in processed_ids:
            continue

        insert_appid(appid)
        save_processed_id(appid)
        print(f"Inserted appid: {appid}")

        count += 1
        if count % 10 == 0:
            print(f"--- Pausing after {count} apps to avoid rate limit ---")
            time.sleep(3)
        else:
            time.sleep(0.5)


if __name__ == "__main__":
    main()
