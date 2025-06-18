import sqlite3
import json
import os
import regex as re
from scrape import scrape

base_dir = os.path.dirname(__file__)
phrase_pattern = r'(?:\p{Lu}\p{L}+\s)+(?:\p{Lu}\p{L}+)'
word_pattern = r'\b\p{Lu}\p{L}+\b'

db_path = os.path.join(base_dir, "..", "data", "tweets.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT text, date FROM tweets ORDER BY date DESC LIMIT 1")
last_tweet = cursor.fetchone()

if last_tweet:
    last_tweet_text, last_tweet_date = last_tweet
    print(f"Last scraped tweet: {last_tweet_text} (Date: {last_tweet_date})")
else:
    last_tweet_text, last_tweet_date = None, None
    print("No previous tweets found, starting fresh.")

# schema_path = os.path.join(base_dir, "..", "data", "schema.sql")

# with open(schema_path, "r") as f:
#     schema = f.read()

# cursor.executescript(schema)
# conn.commit()

all_tweets = scrape(stop_date=last_tweet_date, last_tweet_text=last_tweet_text)
print(f"Scraped {len(all_tweets)} tweets, processing and saving...")

for text, date in all_tweets:
    if text == last_tweet_text and date == last_tweet_date:
        print("Reached the last scraped tweet, stopping scrape process.")
        break
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