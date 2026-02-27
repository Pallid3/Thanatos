import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime, time
import sqlite3

class OsuUser:
    def __init__(self, data):
        self.playcount = int(data["playcount"])
        self.username = data["username"]
        self.pp = float(data["pp_raw"])
        self.timestamp = datetime.utcnow().isoformat()

    def put_data_into_db(self, database):
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        command1 = """CREATE TABLE IF NOT EXISTS
        stats(id INTEGER PRIMARY KEY, username TEXT, playcount INT, pp FLOAT, timestamp TEXT)"""
        cursor.execute(command1)
        # Ainuke tähtis osa. see salvestab andmed stats tabeli (ma loodan) # Only important part, it will save data to the tabel (I hope)
        cursor.execute(
        "INSERT INTO stats (username, playcount, pp, timestamp) VALUES (?, ?, ?, ?)",
        (self.username, self.playcount, self.pp, self.timestamp)
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
    user_data = data[0]

    filtered_data = OsuUser(user_data)
    filtered_data.put_data_into_db(database)
    return
