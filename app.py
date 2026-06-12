from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Jack AI 🤖</h1>

    <input id="msg" placeholder="Type here..." />
    <button onclick="send()">Send</button>

    <p id="reply"></p>

    <script>
    async function send() {
        let message = document.getElementById("msg").value;

        let res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: message})
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

    if "hello" in message.lower():
        reply = "Hello! I'm Jack AI 🤖"
    elif "name" in message.lower():
        reply = "My name is Jack AI"
    else:
        reply = "You said: " + message

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
