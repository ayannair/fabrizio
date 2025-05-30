import sqlite3
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def embed(db_path="tweets.db", index_path="faiss_index"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("")