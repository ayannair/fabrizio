import boto3
import tempfile
import sqlite3
import json
import os
import re

s3_client = boto3.client('s3')

def access_s3(bucket_name, file_name):
    # Using NamedTemporaryFile instead of TemporaryFile
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
        s3_client.download_file(bucket_name, file_name, temp_file_path)
        return temp_file_path

def clean(keyword: str) -> str:
    return re.sub(r'[\"\'\[\]]', '', keyword).strip()

def get_keywords(db_path=None):
    if db_path is None:
        db_path = access_s3('herewegopt', 'tweets.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT keywords FROM tweets")
    rows = cursor.fetchall()
    conn.close()

    words = set()
    for (keyword_list,) in rows:
        if keyword_list:
            try:
                decoded = json.loads(keyword_list)
                cleaned = [clean(kw) for kw in decoded if kw.strip()]
                words.update(cleaned)
            except json.JSONDecodeError:
                continue

    sorted_keywords = sorted(words, key=lambda x: len(x.split()))

    unique_keywords = []
    for keyword in sorted_keywords:
        # Check if any individual word from 'unique_keywords' is contained in the current keyword
        if not any(word in keyword for word in unique_keywords):
            unique_keywords.append(keyword)

    return unique_keywords

if __name__ == "__main__":
    keywords = get_keywords()
    print(json.dumps(keywords, indent=2, ensure_ascii=False))
