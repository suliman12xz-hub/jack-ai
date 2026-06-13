from flask import Flask, request, jsonify, render_template, Response
from openai import OpenAI
import os
import requests

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "wBXNqKUATyqu0RtYt25i"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are Jack AI, a friendly assistant created by Mo. Chat naturally like a normal person. Keep replies short, helpful, and easy to understand."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"reply": reply})

@app.route("/voice", methods=["POST"])
def voice():
    data = request.json
    text = data.get("text", "")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.85
        }
    }

    r = requests.post(url, headers=headers, json=payload)

    if r.status_code != 200:
        print("ELEVENLABS ERROR:", r.status_code, r.text)
        return jsonify({"error": r.text}), 500

    return Response(r.content, mimetype="audio/mpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
