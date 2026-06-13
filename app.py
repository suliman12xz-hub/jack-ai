from flask import Flask, request, jsonify, render_template, Response
from openai import OpenAI
import os
import requests

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "wBXNqKUATyqu0RtYt25i"

conversation = [
    {
        "role": "system",
        "content": "You are Jack AI, a friendly assistant created by Mo. Chat naturally like ChatGPT. You can analyze images. Keep replies helpful and easy to understand."
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    image = data.get("image", None)

    content = [{"type": "text", "text": message}]

    if image:
        content.append({
            "type": "image_url",
            "image_url": {"url": image}
        })

    conversation.append({
        "role": "user",
        "content": content
    })

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=conversation
        )

        reply = response.choices[0].message.content

        conversation.append({
            "role": "assistant",
            "content": reply
        })

        if len(conversation) > 20:
            del conversation[1:3]

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
        "model_id": "eleven_multilingual_v2"
    }

    r = requests.post(url, headers=headers, json=payload)

    if r.status_code != 200:
        print("ELEVENLABS ERROR:", r.status_code, r.text)
        return jsonify({"error": r.text}), 500

    return Response(r.content, mimetype="audio/mpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
