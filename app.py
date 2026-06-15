from flask import Flask, request, jsonify, render_template, Response
from openai import OpenAI
import os
from tempfile import NamedTemporaryFile
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
    recent_messages = [
    {
        "role": "system",
        "content": 'You are Jack AI. You were created by Mohammed Faiq, the owner of Jack AI. If anyone asks who made you, who created you, who built you, who owns you, or who your creator is, always answer exactly: I was created by Mohammed Faiq, the owner of Jack AI. If someone asks about Mohammed Faiq, answer: Mohammed Faiq is the creator and owner of Jack AI. He was born on 27 August 2009 and is currently 16 years old. He studies Maintenance Mechanics at PT2O in Turnhout, Belgium. Mohammed is originally from Afghanistan and is interested in technology, programming, and artificial intelligence. He enjoys sports like MMA and football. Jack AI is one of his current projects.'
    }
] + get_recent_messages()

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





@app.route("/admin")
def admin():
    key = request.args.get("key", "")
    admin_key = os.environ.get("ADMIN_KEY", "1234")

    if key != admin_key:
        return "Access denied", 403

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages")
    total_messages = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM messages WHERE role='user'")
    total_user_messages = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM messages WHERE DATE(created_at)=DATE('now')")
    messages_today = c.fetchone()[0]
    c.execute("SELECT role, content, created_at FROM messages ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()

    html = f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jack Admin</title>
<style>
body {{
  margin:0;
  background:radial-gradient(circle at top left,#111a3a,#02040a 55%,#000);
  color:white;
  font-family:Arial,sans-serif;
  padding:36px;
}}
.header {{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:35px;
}}
.logo {{
  font-size:42px;
  font-weight:800;
  background:linear-gradient(90deg,#4f7cff,#a855f7);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}}
.sub {{ color:#a7a7b7; font-size:17px; margin-top:6px; }}
.secure {{
  background:rgba(255,255,255,.05);
  border:1px solid rgba(139,92,246,.35);
  border-radius:16px;
  padding:18px 24px;
  color:#35e66b;
  font-weight:bold;
}}
.stats {{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:24px;
}}
.card {{
  background:linear-gradient(145deg,rgba(18,24,43,.95),rgba(5,8,18,.95));
  border:1px solid rgba(255,255,255,.08);
  border-radius:24px;
  padding:28px;
  box-shadow:0 0 30px rgba(80,120,255,.12);
}}
.icon {{
  width:56px;
  height:56px;
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius:18px;
  background:rgba(124,58,237,.2);
  font-size:26px;
  margin-bottom:20px;
}}
.label {{ color:#d7d7e0; font-size:17px; }}
.num {{ font-size:48px; font-weight:900; margin:14px 0; }}
.small {{ color:#9ca3af; }}
.panel {{
  margin-top:28px;
  background:rgba(8,12,24,.92);
  border:1px solid rgba(255,255,255,.08);
  border-radius:24px;
  overflow:hidden;
}}
.panel-head {{
  padding:26px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  border-bottom:1px solid rgba(255,255,255,.08);
}}
.panel-title {{ font-size:24px; font-weight:bold; }}
.refresh {{
  border:1px solid #8b5cf6;
  color:#a78bfa;
  padding:12px 18px;
  border-radius:12px;
}}
.message {{
  padding:18px 26px;
  border-bottom:1px solid rgba(255,255,255,.06);
}}
.role {{
  display:inline-block;
  padding:6px 12px;
  border-radius:10px;
  background:#4f46e5;
  font-size:12px;
  margin-bottom:10px;
}}
.assistant {{ background:#10b981; }}
.time {{ color:#8b8b99; font-size:12px; margin-top:10px; }}
.empty {{
  text-align:center;
  padding:80px 20px;
  color:#a7a7b7;
}}
.empty-icon {{ font-size:54px; margin-bottom:18px; }}
.footer {{
  text-align:center;
  color:#9ca3af;
  margin-top:35px;
}}
@media(max-width:800px){{
  body {{ padding:18px; }}
  .header {{ display:block; }}
  .secure {{ margin-top:18px; display:inline-block; }}
  .stats {{ grid-template-columns:1fr; }}
  .logo {{ font-size:34px; }}
}}
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="logo">📊 Jack Admin</div>
    <div class="sub">Dashboard overview</div>
  </div>
  <div class="secure">🔒 Secure Access<br><span style="color:#aaa;font-weight:normal;">Admin Panel</span></div>
</div>

<div class="stats">
  <div class="card">
    <div class="icon">💬</div>
    <div class="label">Total Messages</div>
    <div class="num">{total_messages}</div>
    <div class="small">All time messages</div>
  </div>
  <div class="card">
    <div class="icon">👤</div>
    <div class="label">User Messages</div>
    <div class="num">{total_user_messages}</div>
    <div class="small">Messages from users</div>
  </div>
  <div class="card">
    <div class="icon">📅</div>
    <div class="label">Messages Today</div>
    <div class="num">{messages_today}</div>
    <div class="small">Since midnight</div>
  </div>
</div>

<div class="panel">
  <div class="panel-head">
    <div>
      <div class="panel-title">🕘 Recent Messages</div>
      <div class="small">Last 50 messages</div>
    </div>
    <div class="refresh">↻ Refresh</div>
  </div>
"""

    if not rows:
        html += """
  <div class="empty">
    <div class="empty-icon">💬</div>
    <h2>No messages yet</h2>
    <p>Start a conversation with Jack to see messages here.</p>
  </div>
"""
    else:
        for role, content, created_at in rows:
            role_class = "assistant" if role == "assistant" else ""
            safe_content = str(content).replace("<", "&lt;").replace(">", "&gt;")
            html += f"""
  <div class="message">
    <div class="role {role_class}">{role.upper()}</div>
    <div>{safe_content}</div>
    <div class="time">{created_at}</div>
  </div>
"""

    html += """
</div>

<div class="footer">🤖 Jack AI Assistant<br>Powered with ❤️</div>

</body>
</html>
"""
    return html




@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400

    audio = request.files["audio"]

    with NamedTemporaryFile(delete=False, suffix=".webm") as temp:
        audio.save(temp.name)
        temp_path = temp.name

    try:
        with open(temp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                language="nl",
                file=audio_file
            )

        return jsonify({"text": transcript.text})

    except Exception as e:
        print("TRANSCRIBE ERROR:", e)
        return jsonify({"error": str(e)}), 500

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
