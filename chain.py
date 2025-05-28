import os
import sqlite3
import json
import regex as re
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

load_dotenv()

def get_tweets(entity: str, db_path: str = 'tweets.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT text, date FROM tweets WHERE keywords LIKE ?"
    cursor.execute(query, (f'%{entity}%',))
    rows = cursor.fetchall()
    conn.close()
    return rows

def format(rows):
    if not rows:
        return "No tweets found"
    context = ""
    for text, date in rows:
        context += f"[{date}] {text}\n\n"
    return context

def generate_summary(entity: str, context: str) -> str:
    llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
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
    entity = input("Enter an entity name (e.g. Jack Grealish, Bayer Leverkusen): ").strip()
    tweets = get_tweets(entity)
    context = format(tweets)

    if context == "No tweets found.":
        print(context)
    else:
        summary = generate_summary(entity, context)
        print("\nSummary:\n")
        print(summary)