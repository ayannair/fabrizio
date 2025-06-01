import os
import sys
import sqlite3
import json
import regex as re
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def load_index(index_path=None):
    if index_path is None:
        base_dir = os.path.dirname(__file__)  # path to backend/
        index_path = os.path.join(base_dir, "..", "data", "faiss_index")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

def get_tweets(entity: str, k: int = 5):
    faiss_index = load_index()
    docs = faiss_index.similarity_search(entity, k=k)
    filtered = [
        (doc.page_content, doc.metadata.get("date", "Unknown"))
        for doc in docs
        if entity.lower() in doc.page_content.lower()
        or entity.lower() in [kw.lower() for kw in doc.metadata.get("keywords", [])]
    ]
    return filtered

def format(rows):
    if not rows:
        return "No tweets found"
    context = ""
    for text, date in rows:
        context += f"[{date}] {text}\n\n"
    return context

def generate_summary(entity: str, context: str) -> str:
    llm = init_chat_model("gpt-3.5-turbo", model_provider="openai")
    prompt = PromptTemplate(
        input_variables=["entity", "context"],
        template=(
            "You are a football analyst.\n\n"
            "Given the following tweets about {entity}, summarize their current situation. "
            "Focus on any recent transfer rumors, injuries, management changes, or rumors. "
            "Be specific, and only use what’s in the tweets.\n\n"
            "Tweets:\n"
            "{context}\n"
            "Summary:"
        )
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({"entity": entity, "context": context})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        entity = " ".join(sys.argv[1:]).strip()
    else:
        entity = input("Enter an entity name (e.g. Jack Grealish, Bayer Leverkusen): ").strip()

    tweets = get_tweets(entity)
    context = format(tweets)
    if context == "No tweets found":
        print(context)
    else:
        summary = generate_summary(entity, context)
        print("\nSummary:\n")
        print(summary)