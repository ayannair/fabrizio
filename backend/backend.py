from flask import Flask, jsonify, request
from keywords import get_keywords
from chain import get_tweets, generate_summary, generate_timeline, format
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/api/keywords", methods=["GET"])
def keywords():
    try:
        keywords_list = get_keywords()
        return jsonify(keywords_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/query", methods=["GET"])
def query():
    try:
        entity = request.args.get('entity', '')
        if not entity:
            return jsonify({"error": "No entity provided"}), 400

        tweets = get_tweets(entity)
        context = format(tweets)
        if context == "No tweets found":
            return jsonify({"summary": context, "tweets": []})
        
        summary = generate_summary(entity, context)
        timeline = generate_timeline(tweets)
        
        return jsonify({"summary": summary, "timeline": timeline})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))