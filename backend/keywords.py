import sqlite3
import json
import os
import re

def clean(keyword: str) -> str:
    return re.sub(r'[\"\'\[\]]', '', keyword).strip()

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
            try:
                decoded = json.loads(keyword_list)
                cleaned = [clean(kw) for kw in decoded if kw.strip()]
                words.update(cleaned)
            except json.JSONDecodeError:
                continue

    return sorted(words)

if __name__ == "__main__":
    keywords = get_keywords()
    print(json.dumps(keywords, indent=2, ensure_ascii=False))
