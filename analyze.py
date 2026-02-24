import sqlite3, os

def username_exists(username, database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT 1 FROM stats WHERE username = ? LIMIT 1",
        (username,)
    )
    exists = cursor.fetchone() is not None
    connection.close()
    return exists

def compare_last_two_db(username, database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    # Get all entries for this user, ordered by timestamp
    cursor.execute(
        "SELECT playcount, timestamp FROM stats WHERE username = ? ORDER BY id ASC",
        (username,)
    )
    rows = cursor.fetchall()
    connection.close()

    if len(rows) < 2:
        print("Not enough data to compare from", username)
        return None

    # Take the last two playcounts
    playcount1 = rows[-2][0]  # second-to-last
    playcount2 = rows[-1][0]  # last

    return playcount2 - playcount1

# Example usage:
# diff = compare_last_two_db("kellad")
# print("Playcount increase:", diff)