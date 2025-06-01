import sqlite3
import json
import os
import re

def clean(keyword: str) -> str:
    return re.sub(r'[\"\'\[\]]', '', keyword).strip().lower()

def get_keywords(db_path=None) -> list[str]:
    if db_path is None:
        base_dir = os.path.dirname(__file__)  # backend/
        db_path = os.path.join(base_dir, "..", "data", "tweets.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT keywords FROM tweets")
    rows = cursor.fetchall()
    conn.close()

    words = set()
    for (keyword_list,) in rows:
        if keyword_list:
            raw = keyword_list.split(",")
            cleaned = [clean(kw) for kw in raw if kw.strip()]
            words.update(cleaned)

    return sorted(words)

if __name__ == "__main__":
    keywords = get_keywords()
    print(json.dumps(keywords, indent=2))
