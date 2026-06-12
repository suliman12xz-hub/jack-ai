@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").lower()

    if "hello" in message or "hallo" in message:
        reply = "Hello! I'm Jack AI 🤖"
    elif "how are you" in message:
        reply = "I'm good! How can I help you?"
    elif "who are you" in message:
        reply = "I'm Jack AI, your assistant."
    else:
        reply = "I don't know yet, but I'm learning."

    return jsonify({"reply": reply})
