import sqlite3
import json

def jsonl_to_db(jsonl_file="osu_user.jsonl", db_file="oss_stats.db"):
    # Connect to (or create) new database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Create the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats(
            id INTEGER PRIMARY KEY,
            username TEXT,
            playcount INT,
            pp FLOAT,
            timestamp TEXT
        )
    """)

    # Read JSONL file and insert each entry
    with open(jsonl_file, "r") as f:
        for line in f:
            data = json.loads(line)
            cursor.execute(
                "INSERT INTO stats (username, playcount, pp, timestamp) VALUES (?, ?, ?, ?)",
                (data["username"], data["playcount"], data["pp"], data["timestamp"])
            )

    connection.commit()
    connection.close()
    print(f"Migration complete! Data stored in {db_file}")

# Example usage: # Please use it only once, cuz it will dubilcate shit.
# jsonl_to_db()