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

    def to_dict(self):
        return {
            "username": self.username,
            "playcount": self.playcount,
            "pp": self.pp,
            "timestamp": self.timestamp
        }

    def pane_andmed_baasi(self, andmebaas):
        connection = sqlite3.connect(andmebaas)
        cursor = connection.cursor()

        command1 = """CREATE TABLE IF NOT EXISTS
        stats(id INTEGER PRIMARY KEY, username TEXT, playcount INT, pp FLOAT, timestamp TEXT)"""
        cursor.execute(command1)
        # Ainuke tähtis osa. see salvestab andmed stats tabeli (ma loodan)
        cursor.execute(
        "INSERT INTO stats (username, playcount, pp, timestamp) VALUES (?, ?, ?, ?)",
        (self.username, self.playcount, self.pp, self.timestamp)
        )
        connection.commit()
        connection.close()

    @classmethod
    def from_dict(cls, data):
        obj = cls.__new__(cls)
        obj.username = data["username"]
        obj.playcount = data["playcount"]
        obj.pp = data["pp"]
        return obj

def make_user_request(username, API_KEY, andmebaas):
    # username = "kellad"         # or a numeric user ID
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
    filtered_data.pane_andmed_baasi(andmebaas)


    # with open("osu_user.jsonl", "a") as f:
    #     json.dump(filtered_data.to_dict(), f)
    #     f.write("\n")
    return

def read_data():
    entries = []
    with open("osu_user.jsonl", "r") as f:
        for line in f:
            entries.append(json.loads(line))
    return entries


load_dotenv()
API_KEY = os.getenv('OSU_API_KEY')


make_user_request("kellad", API_KEY)