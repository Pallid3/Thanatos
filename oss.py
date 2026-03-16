import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime, time
import sqlite3

class OsuUser:
    def __init__(self, data, gamemode_int):
        self.playcount = int(data["playcount"])
        self.username = data["username"]
        self.pp = float(data["pp_raw"])
        self.timestamp = datetime.utcnow().isoformat()
        self.gamemode = int(gamemode_int)

    def put_data_into_db(self, database):
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        command1 = """CREATE TABLE IF NOT EXISTS
        gamemode_stats(id INTEGER PRIMARY KEY, username TEXT, playcount INT, pp FLOAT, timestamp TEXT, gamemode INT)"""
        cursor.execute(command1)
        # Ainuke tähtis osa. see salvestab andmed stats tabeli (ma loodan) # Only important part, it will save data to the tabel (I hope)
        cursor.execute(
        "INSERT INTO gamemode_stats (username, playcount, pp, timestamp, gamemode) VALUES (?, ?, ?, ?, ?)",
        (self.username, self.playcount, self.pp, self.timestamp, self.gamemode)
        )
        connection.commit()
        connection.close()


def make_user_request(username, API_KEY, database):
    # username = "kellad"
    username = str(username)
    API_KEY = str(API_KEY)

    url = "https://osu.ppy.sh/api/get_user"
    params = {
        "k": API_KEY,
        "u": username,
        "m": 0   # mode 0 = osu!standard
    }

    response = requests.get(url, params=params)
    data = response.json()
    if not data:
        print(f"No data returned for {username}")
        return
    user_data = data[0]

    filtered_data = OsuUser(user_data, params["m"])
    filtered_data.put_data_into_db(database)
    return

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    API_KEY = os.getenv('OSU_API_KEY')

    database = "oss_tests.db"
    make_user_request(username="kellad", API_KEY=API_KEY, database=database)
