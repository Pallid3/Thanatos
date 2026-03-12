CREATE TABLE IF NOT EXISTS gamemode_stats (
    id INTEGER PRIMARY KEY,
    username TEXT,
    playcount INT,
    pp FLOAT,
    timestamp TEXT,
    gamemode INT
);

INSERT INTO gamemode_stats (username, playcount, pp, timestamp, gamemode)
SELECT username, playcount, pp, timestamp, 0
FROM stats;