@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower()

    if "hello" in message:
        reply = "Hello! I'm Jack AI 🤖"
    elif "name" in message:
        reply = "My name is Jack AI"
    elif "how are you" in message:
        reply = "I'm doing great 😄 Thanks for asking!"
    elif "what" in message and "your name" in message:
        reply = "My name is Jack AI"
    elif "how are you" in message:
        reply = "I'm fine 👍 and you?"
    else:
        reply = "I understand: " + message

    return jsonify({"reply": reply})
