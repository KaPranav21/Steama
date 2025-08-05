import os
import requests
from dotenv import load_dotenv
from db import init_db, insert_game

load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_API_KEY')

DB_CONFIG = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'steam_project'),
}

def fetch_all_apps():
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['applist']['apps']

def fetch_app_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if data[str(appid)]['success']:
        details = data[str(appid)]['data']
        developer = details.get('developers', ['Unknown'])[0] if 'developers' in details else 'Unknown'
        release_date = details.get('release_date', {}).get('date', 'Unknown') if 'release_date' in details else 'Unknown'
        type_ = details.get('type', 'Unknown')
        name = details.get('name', 'Unknown')
        return appid, name, developer, release_date, type_
    else:
        return None

def main():
    init_db()  # Create the table if not exists

    apps = fetch_all_apps()
    print(f"Total apps fetched: {len(apps)}")

    # For demo, just fetch details for first 50 apps to avoid API spam
    for app in apps[:50]:
        appid = app['appid']
        details = fetch_app_details(appid)
        if details:
            insert_game(*details)
            print(f"Inserted game {details[1]} (appid: {appid})")
        else:
            print(f"Skipping appid {appid} - no details found")

if __name__ == "__main__":
    main()
