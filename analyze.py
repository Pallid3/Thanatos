import oss

def compare_last_two():
    ents = oss.read_data()
    sorted_data = sorted(ents, key=lambda x: x['timestamp'])
    latest_two = sorted_data[-2:]
    playcount1 = latest_two[0]['playcount']
    playcount2 = latest_two[1]['playcount']

    # print("Latest two playcounts:", playcount1, playcount2)
    return playcount2 - playcount1

