from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return """
    <h1>Jack AI 🤖</h1>

    <input id="msg" placeholder="Type..." />
    <button onclick="send()">Send</button>

    <p id="reply"></p>

    <script>
    async function send() {
        let message = document.getElementById("msg").value;

        let res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });

        let data = await res.json();
        document.getElementById("reply").innerText = data.reply;
    }
    </script>
    """

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Jack AI, a friendly assistant."},
            {"role": "user", "content": message}
        ]
    )

    reply = response.choices[0].message.content

    return jsonify({"reply": reply})
