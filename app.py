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