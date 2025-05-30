import sqlite3
import faiss
from uuid import uuid4
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

def embed(db_path="tweets.db", index_path="faiss_index"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, date FROM tweets")
    data = cursor.fetchall()
    print(data[:5])
    conn.close()

    documents = [Document(page_content=text, metadata={"id": str(id_), "date": date}) for id_, text, date in data]

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)
    vector_store.save_local(index_path)
    print(f"Embedded {len(documents)} tweets and saved FAISS index to '{index_path}'")


if __name__ == "__main__":
    embed()
