import requests
import sqlite3
import time
import os
from dotenv import load_dotenv

# Load API key from .env if needed
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

DB_NAME = "steam_games.db"
PROCESSED_FILE = "processed_ids.txt"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            appid INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            is_free INTEGER,
            short_description TEXT
        )
    ''')
    conn.commit()
    conn.close()


def fetch_all_apps():
    response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    response.raise_for_status()
    data = response.json()
    return data['applist']['apps']


def fetch_app_details(appid, retries=3):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 429:
                print(f"Rate limited on appid {appid}. Waiting...")
                time.sleep(3)
                continue

            response.raise_for_status()
            data = response.json()
            app_data = data[str(appid)]

            if not app_data.get("success", False):
                return None

            details = app_data["data"]
            return (
                appid,
                details.get("name", ""),
                details.get("type", ""),
                int(details.get("is_free", False)),
                details.get("short_description", "")
            )
        except Exception as e:
            print(f"Error fetching appid {appid}: {e}")
            time.sleep(1)
    return None


def insert_game(appid, name, type_, is_free, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO games (appid, name, type, is_free, short_description)
        VALUES (?, ?, ?, ?, ?)
    ''', (appid, name, type_, is_free, description))
    conn.commit()
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
    init_db()
    processed_ids = load_processed_ids()
    apps = fetch_all_apps()
    print(f"Total apps fetched: {len(apps)}")

    count = 0
    for app in apps:
        appid = app['appid']

        if appid in processed_ids:
            continue

        details = fetch_app_details(appid)
        if details:
            insert_game(*details)
            save_processed_id(appid)
            print(f"Inserted game: {details[1]} (appid: {appid})")
        else:
            print(f"Skipping appid {appid} - no details")

        count += 1
        if count % 10 == 0:
            print(f"--- Pausing after {count} apps to avoid rate limit ---")
            time.sleep(3)
        else:
            time.sleep(0.5)  # Light delay to prevent rate limiting

        # Optional: Limit total for now
        if count >= 100:
            print("Reached limit of 100 apps (demo run).")
            break


if __name__ == "__main__":
    main()
