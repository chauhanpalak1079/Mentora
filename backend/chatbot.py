import google.generativeai as genai
from flask import Blueprint, request, jsonify
from database import get_db_connection
from config import Config
from auth import verify_jwt
from database import fetch_chat_history, get_user_name  , get_username_by_id


chatbot_bp = Blueprint("chatbot", __name__)
genai.configure(api_key=Config.GEMINI_API_KEY)

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    user_id = verify_jwt(token.split(" ")[1])
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    message = data.get('message')
    print(user_id)
    # Retrieve username
    conn = get_db_connection()
    cursor = conn.cursor()
    
    username = get_username_by_id(user_id)
    
    print(username)

    # Generate chatbot response using Gemini 1.5 Pro
    r= generate_response(username, message)
    bot_response = r.strip()  # Extract text response

    # Store user message & bot response in the same row
    cursor.execute("INSERT INTO chat_history (username, user_message, bot_response) VALUES (?, ?, ?)", 
                   (username, message, bot_response))

    conn.commit()
    conn.close()
    print (bot_response)
    return jsonify({"response": bot_response})

@chatbot_bp.route('/chat/history', methods=['GET'])
def get_chat_history():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    user_id = verify_jwt(token.split(" ")[1])
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Get the username from user_id
    conn = get_db_connection()
    cursor = conn.cursor()

    username= get_username_by_id(user_id)

    # Retrieve chat history
    cursor.execute("SELECT user_message, bot_response, timestamp FROM chat_history WHERE username = ? ORDER BY timestamp ASC", (username,))
    chat_logs = cursor.fetchall()
    conn.close()
    print("Fetched history from DB:", chat_logs)  # Debugging log
    return jsonify({
        "history": [
            {"user_message": log[0], "bot_response": log[1], "timestamp": log[2]} for log in chat_logs
        ]
    })

def generate_response(username, message):
    """Generate chatbot response while remembering past conversations and user name."""

    # 🔹 Fetch the user's real name
    user_name = get_user_name(username)
    greeting = f"Hello {user_name}," if user_name else "Hello,"

    # 🔹 Fetch last 5 messages from chat history
    chat_history = fetch_chat_history(username, limit=5)
    
    # 🔹 Format chat history for prompt
    formatted_history = "\n".join([
        f"User: {msg['user_message']}\nAssistant: {msg['bot_response']}" for msg in chat_history
    ])

    # 🔹 Create a prompt including user name and chat history
    prompt = f"""
    You are **Mentora**, a Mood Journal Assistant and Meditation Coach.
    Your job is to help users reflect on emotions and provide relaxation exercises.

    {greeting} Here’s the past conversation:
    {formatted_history}

    Now, continue the conversation:
    User: {message}
    Assistant:
    """

    # 🔹 Generate response using Gemini AI
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt, generation_config={"temperature": 0.7, "max_output_tokens": 300})

    

    return response.text
