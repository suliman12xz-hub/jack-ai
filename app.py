from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").lower()

    if "hello" in message or "hallo" in message:
        reply = "Hello! I'm Jack AI 🤖"
    elif "who are you" in message:
        reply = "I'm Jack AI, your assistant."
    elif "how are you" in message:
        reply = "I'm doing great!"
    else:
        reply = f"You said: {message}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
