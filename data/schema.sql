-- DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    date TEXT,
    keywords TEXT
);