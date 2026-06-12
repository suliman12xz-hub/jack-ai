@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # simpele "AI brain"
    if "hello" in user_message.lower():
        reply = "Hello! I'm Jack AI 🤖"
    elif "your name" in user_message.lower():
        reply = "My name is Jack AI"
    elif "how are you" in user_message.lower():
        reply = "I'm doing great! Thanks for asking 😊"
    else:
        reply = f"I heard: {user_message}"

    return jsonify({"reply": reply})
