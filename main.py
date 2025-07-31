import os
import requests
import time
import csv
from dotenv import load_dotenv

load_dotenv()

# Fetch App Details from Steam API
def get_app_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get(str(appid), {}).get("success"):
                return data[str(appid)]["data"]
    except Exception as e:
        print(f"Error fetching AppID {appid}: {e}")
    return None

def main():
    output_file = "steam_games.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["AppID", "Name", "Developer", "Release Date", "Type"])  # CSV header

        for appid in range(0, 101):
            details = get_app_details(appid)

            if details and details.get("type") == "game":
                name = details.get("name", "Unknown")
                developer = details.get("developers", ["Unknown"])[0]
                release_date = details.get("release_date", {}).get("date", "Unknown")
                type_ = details.get("type", "Unknown")

                print(f"[{appid}] {name} | {developer} | {release_date}")
                writer.writerow([appid, name, developer, release_date, type_])
            else:
                print(f"[{appid}] empty ID.")

            time.sleep(0.1)

if __name__ == "__main__":
    main()
