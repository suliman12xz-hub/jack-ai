from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Jack AI, a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )

    reply = response.choices[0].message.content

    return jsonify({"reply": reply})
