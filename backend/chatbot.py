import google.generativeai as genai
from flask import Blueprint, request, jsonify, session
from database import get_db_connection
from config import Config

chatbot_bp = Blueprint("chatbot", __name__)
genai.configure(api_key=Config.GEMINI_API_KEY)

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = session.get("user_id")
    user_input = data.get("message", "").strip()

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if not user_input:
        return jsonify({"response": "Please type a message."})

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(f"""
    You are **Mentora**, a friendly mental health assistant. 
    Always provide empathetic, clear, and supportive responses.

    User: {user_input}
    Assistant:
    """, 
    generation_config={"temperature": 0.7, "max_output_tokens": 100}
    )

    bot_reply = response.text.strip()

    # Store conversation in DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (?, ?, ?)", (user_id, user_input, bot_reply))
    conn.commit()
    conn.close()

    return jsonify({"response": bot_reply})
