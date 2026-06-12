from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    return jsonify({"reply": "TEST OK: " + message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
