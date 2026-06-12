from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <body>
        <h1>Jack AI</h1>

        <input id="msg" placeholder="Type hier...">
        <button onclick="send()">Send</button>

        <div id="chat"></div>

        <script>
        async function send() {
            let msg = document.getElementById("msg").value;

            let response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({message: msg})
            });

            let data = await response.json();

            document.getElementById("chat").innerHTML +=
                "<p><b>Jij:</b> " + msg + "</p>" +
                "<p><b>Jack:</b> " + data.reply + "</p>";
        }
        </script>
    </body>
    </html>
    """

@app.route("/chat", methods=["POST"])
def chat():
    from flask import request, jsonify

    data = request.json
    message = data.get("message", "")

    if "how are you" in message.lower():
        reply = "I'm good! How can I help you?"
    else:
        reply = "Hello!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
