from flask import Flask, request, jsonify, render_template, Response
from openai import OpenAI
import os
import requests
import sqlite3

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "wBXNqKUATyqu0RtYt25i"

DB_NAME = "jack_memory.db"

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are Jack AI, a modern AI assistant created by Mo. Write naturally like ChatGPT. Use clean formatting and short paragraphs. Use headings and bullet points only when useful. Use at most 1 or 2 emojis per answer. Make responses look professional, modern and easy to read. Avoid giant walls of text."
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_message(role, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

def get_recent_messages(limit=12):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()

    rows.reverse()
    return [{"role": role, "content": content} for role, content in rows]

def get_memory_text():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT key, value FROM memory ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "No saved memory yet."

    return "\\n".join([f"{key}: {value}" for key, value in rows])

def remember_from_message(message):
    lower = message.lower()

    # Simple memory commands
    if lower.startswith("remember that "):
        value = message[len("remember that "):].strip()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO memory (key, value) VALUES (?, ?)", ("note", value))
        conn.commit()
        conn.close()
        return True

    if lower.startswith("my name is "):
        value = message[len("my name is "):].strip()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO memory (key, value) VALUES (?, ?)", ("name", value))
        conn.commit()
        conn.close()
        return True

    return False

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    print("USER SEARCHED:", message)
    image = data.get("image", None)

    remember_from_message(message)

    save_message("user", message)

    memory_text = get_memory_text()
    recent_messages = get_recent_messages()

    messages = [
        SYSTEM_PROMPT,
        {
            "role": "system",
            "content": "Saved memory about the user:\\n" + memory_text
        }
    ]

    messages.extend(recent_messages)

    content = [{"type": "text", "text": message}]

    if image:
        content.append({
            "type": "image_url",
            "image_url": {"url": image}
        })

    messages.append({
        "role": "user",
        "content": content
    })

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        reply = response.choices[0].message.content

        save_message("assistant", reply)

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"reply": reply})

@app.route("/memory", methods=["GET"])
def memory():
    return jsonify({"memory": get_memory_text()})

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
