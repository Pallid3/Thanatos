import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime, time

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

    @classmethod
    def from_dict(cls, data):
        obj = cls.__new__(cls)
        obj.username = data["username"]
        obj.playcount = data["playcount"]
        obj.pp = data["pp"]
        return obj

def make_user_request(username, API_KEY):
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
    with open("osu_user.jsonl", "a") as f:
        json.dump(filtered_data.to_dict(), f)
        f.write("\n")
    return

def read_data():
    entries = []
    with open("osu_user.jsonl", "r") as f:
        for line in f:
            entries.append(json.loads(line))
    return entries

print("test")