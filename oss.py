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

# load_dotenv()
# token = os.getenv('DISCORD_TOKEN')
# API_KEY = os.getenv('OSU_API_KEY')


# make_user_request("kellad", API_KEY)

# aaa = read_data()
# print(aaa)
# sorted_data = sorted(aaa, key=lambda x: x['timestamp'])
# latest_two = sorted_data[-2:]
# playcount1 = latest_two[0]['playcount']
# playcount2 = latest_two[1]['playcount']


# print("Latest two playcounts:", playcount1, playcount2)

# if playcount2 > playcount1:
#     print("Playcount increased by", playcount2 - playcount1)
# elif playcount2 < playcount1:
#     print("Playcount decreased by", playcount1 - playcount2)
# else:
#     print("Playcount did not change")





# for e in entries:
#     e["timestamp"] = datetime.fromisoformat(e["timestamp"])
# latest = max(entries, key=lambda e: e["timestamp"])

# print(latest)
# print(latest["playcount"])
