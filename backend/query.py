import sqlite3
import json

conn = sqlite3.connect('../data/tweets.db')
cursor = conn.cursor()

search_term = "Liverpool"
query = "SELECT text, date, keywords FROM tweets WHERE keywords LIKE ?"
cursor.execute(query, (f'%{search_term}%',))

results = cursor.fetchall()

for text, date, keywords_json in results:
    keywords = json.loads(keywords_json)
    print(f"Date: {date}")
    print(f"Keywords: {keywords}")
    print(f"Tweet: {text}")
    print("-" * 40)

conn.close()