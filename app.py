from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Jack AI 🤖</h1>

    <input id="msg" placeholder="Type something..." />
    <button onclick="send()">Send</button>

    <p id="reply"></p>

    <script>
    async function send() {
        let message = document.getElementById("msg").value;

        let res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });

        let data = await res.json();
        document.getElementById("reply").innerText = data.reply;
    }
    </script>
    """

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    return jsonify({"reply": "Jack AI: " + message})

if __name__ == "__main__":
    app.run()
