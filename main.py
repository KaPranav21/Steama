import csv
from db import init_db, insert_game

csv_path = "steam_games.csv"

def load_steam_data(csv_file):
    games = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            appid = int(row["AppID"])
            name = row["Name"]
            developer = row["Developer"]
            release_date = row["Release Date"]
            type_ = row["Type"]
            games.append((appid, name, developer, release_date, type_))
    return games

def main():
    init_db()
    games = load_steam_data(csv_path)

    for game in games:
        insert_game(*game)

    print(f"Inserted {len(games)} games into the database.")

if __name__ == "__main__":
    main()
