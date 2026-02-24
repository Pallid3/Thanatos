import sqlite3

def username_exists(username, db_file="oss_stats.db"):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT 1 FROM stats WHERE username = ? LIMIT 1",
        (username,)
    )
    exists = cursor.fetchone() is not None
    connection.close()
    return exists

def compare_last_two_db(username):
    connection = sqlite3.connect("oss_stats.db")
    cursor = connection.cursor()

    # Get all entries for this user, ordered by timestamp
    cursor.execute(
        "SELECT playcount, timestamp FROM stats WHERE username = ? ORDER BY timestamp ASC",
        (username,)
    )
    rows = cursor.fetchall()
    connection.close()

    if len(rows) < 2:
        raise ValueError("Not enough data to compare from", username)

    # Take the last two playcounts
    playcount1 = rows[-2][0]  # second-to-last
    playcount2 = rows[-1][0]  # last

    return playcount2 - playcount1

# Example usage:
# diff = compare_last_two_db("kellad")
# print("Playcount increase:", diff)