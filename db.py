import sqlite3
import json
import regex as re
from scrape import scrape

phrase_pattern = r'(?:\p{Lu}\p{L}+\s)+(?:\p{Lu}\p{L}+)'
word_pattern = r'\b\p{Lu}\p{L}+\b'

conn = sqlite3.connect("tweets.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    date TEXT,
    keywords TEXT
)
''')
conn.commit()

all_tweets = scrape()
print(f"Scraped {len(all_tweets)} tweets, processing and saving...")

for text, date in all_tweets:
    phrases = set(re.findall(phrase_pattern, text))
    words = set(re.findall(word_pattern, text))
    phrase_words = set(word for phrase in phrases for word in phrase.split())
    words = words - phrase_words
    keywords = list(phrases.union(words))  # convert to list for JSON

    keywords_json = json.dumps(keywords)

    cursor.execute('''
    INSERT INTO tweets (text, date, keywords) VALUES (?, ?, ?)
    ''', (text, date, keywords_json))

conn.commit()
conn.close()

print("Success!")