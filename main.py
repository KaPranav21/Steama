import os
import requests
from dotenv import load_dotenv

# Load the environment variables from .env
load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# Replace with any public SteamID or your own
STEAM_ID = "76561197960435530"  # Example ID (Gabe Newell's account)

def get_owned_games(steam_id):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steam_id,
        "include_appinfo": True,
        "format": "json"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    games_data = get_owned_games(STEAM_ID)
    if games_data:
        print("Owned games data:")
        print(games_data)
