@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").lower()

    if "hello" in message or "hi" in message:
        reply = "Hello! I'm Jack AI 🤖"

    elif "how are you" in message:
        reply = "I'm doing great! How are you?"

    elif "who are you" in message:
        reply = "I'm Jack AI, your personal assistant."

    elif "your name" in message:
        reply = "My name is Jack AI."

    elif "time" in message:
        from datetime import datetime
        reply = "Current time: " + datetime.now().strftime("%H:%M")

    elif "weather" in message:
        reply = "I can't check live weather yet."

    elif "help" in message:
        reply = "I can answer basic questions and chat with you."

    else:
        reply = "That's interesting. Tell me more."

    return jsonify({"reply": reply})
