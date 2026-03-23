from flask import Flask, request, jsonify, render_template
import requests, os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user = request.json["message"]

    chat_history.append({"role": "user", "content": user})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openchat/openchat-3.5",
            "messages": chat_history
        }
    )

    data = response.json()

    if "choices" not in data:
        return jsonify({"reply": "Error: API issue"})

    reply = data["choices"][0]["message"]["content"]

    chat_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
