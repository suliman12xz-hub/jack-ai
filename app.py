from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Jack AI is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if "hello" in user_message.lower():
        reply = "Hello! I'm Jack AI 🤖"
    elif "name" in user_message.lower():
        reply = "My name is Jack AI"
    else:
        reply = f"You said: {user_message}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
