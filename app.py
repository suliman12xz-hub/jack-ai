from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").lower()

    if "hello" in message or "hi" in message or "hallo" in message:
        reply = "Hello! I'm Jack AI 🤖"

    elif "how are you" in message:
        reply = "I'm doing great! How are you?"

    elif "who are you" in message:
        reply = "I'm Jack AI, your personal assistant."

    elif "who made you" in message:
        reply = "I was created by Mo 😎"

    elif "joke" in message:
        reply = "Why don't programmers like nature? It has too many bugs! 😂"

    elif "time" in message:
        reply = "Current time: " + datetime.now().strftime("%H:%M")

    elif "date" in message:
        reply = datetime.now().strftime("%d/%m/%Y")

    elif message.replace("+","").isdigit() and "+" in message:
        nums = message.split("+")
        reply = str(int(nums[0]) + int(nums[1]))

    elif "what can you do" in message:
        reply = "I can chat, tell jokes, show time and solve simple math."

    elif "+" in message:
        try:
            a,b = message.split("+")
            reply = str(float(a) + float(b))
        except:
            reply = "Math error"

    elif "-" in message:
        try:
            a,b = message.split("-")
            reply = str(float(a) - float(b))
        except:
            reply = "Math error"

    elif "*" in message:
        try:
            a,b = message.split("*")
            reply = str(float(a) * float(b))
        except:
            reply = "Math error"

    elif "/" in message:
        try:
            a,b = message.split("/")
            reply = str(float(a) / float(b))
        except:
            reply = "Math error"

    else:
        reply = "I don't know that yet, but Mo can teach me! 🚀"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
