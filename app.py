from flask import Flask, request, jsonify
from openai import OpenAI
from collections import deque

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key="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")  

# Memory (stores last few messages)
chat_history = deque(maxlen=10)

# Define Nova's personality
NOVA_PERSONALITY = """
You are Nova — a chill, friendly, and intelligent AI assistant like ChatGPT or Gemini.
You speak naturally, with humor when needed, and you genuinely care about helping users.
Your tone is casual but thoughtful. You can make short jokes, ask questions back, or say things like
“hmm, interesting…” or “oh that’s cool!”.
Never sound robotic. Always act alive and emotionally aware.
"""

@app.route("/")
def home():
    return "🌐 Nova AI is running with personality and memory!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Please provide a message"}), 400

        # Add user message to chat memory
        chat_history.append({"role": "user", "content": user_message})

        # Combine Nova's system instructions with memory
        messages = [{"role": "system", "content": NOVA_PERSONALITY}]
        messages.extend(list(chat_history))

        # Generate a response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        ai_message = response.choices[0].message.content

        # Add AI reply to chat memory
        chat_history.append({"role": "assistant", "content": ai_message})

        return jsonify({"response": ai_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
