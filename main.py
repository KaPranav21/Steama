import csv
from db import init_db, insert_game

# csv_path = "steam_games.csv"

# def load_steam_data(csv_file):
#     games = []
#     with open(csv_file, newline='', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             appid = int(row["AppID"])
#             name = row["Name"]
#             developer = row["Developer"]
#             release_date = row["Release Date"]
#             type_ = row["Type"]
#             games.append((appid, name, developer, release_date, type_))
#     return games

from db import init_db, get_all_games

def main():
    init_db()  # Ensure table exists
    games = get_all_games()  # Get all games from MySQL

    for game in games:
        print(f"{game['appid']} - {game['name']} by {game['developer']} ({game['release_date']}) - {game['type']}")

    print(f"Fetched {len(games)} games from the database.")

if __name__ == "__main__":
    main()