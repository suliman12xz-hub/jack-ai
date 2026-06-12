from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Jack AI is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    reply = f"Jack AI says: you said '{user_message}'"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
