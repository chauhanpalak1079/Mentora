import google.generativeai as genai
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
from flask_session import Session

app = Flask(__name__)
CORS(app)

# Configure Flask Session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "fucking_do_it_pr0prely"
Session(app)

# Set your Google Gemini API Key
genai.configure(api_key="AIzaSyBcfVY6OI_pQdROE-CCgMb1hLgKXukWya0")  # Replace with your key


# Initialize Database for Long-Term Memory
def init_db():
    conn = sqlite3.connect("chat_memory.db")  # Creates the DB file if not exists
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            role TEXT  -- 'user' or 'assistant'
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Ensure DB is set up when app starts

# Function to Save Chat to Database
def save_message(user_id, message, role):
    conn = sqlite3.connect("chat_memory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, message, role) VALUES (?, ?, ?)", 
                   (user_id, message, role))
    conn.commit()
    conn.close()

# Function to Retrieve Past Chats (Long-Term Memory)
def get_chat_history(user_id, limit=10):
    conn = sqlite3.connect("chat_memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT message, role FROM chat_history WHERE user_id = ? ORDER BY id DESC LIMIT ?", 
                   (user_id, limit))
    messages = cursor.fetchall()
    conn.close()
    
    # Format chat history for AI model
    chat_history = [f"{'User' if role == 'user' else 'Assistant'}: {msg}" for msg, role in reversed(messages)]
    return "\n".join(chat_history)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_input = data.get("message", "").strip()
    user_id = data.get("user_id", "default_user")  # Unique user identifier

    if not user_input:
        return jsonify({"response": "I'm here to help! Could you clarify your question?"})

    # Save User Message to Long-Term Memory (DB)
    save_message(user_id, user_input, "user")

    # Retrieve Last 10 Messages (Long-Term Memory)
    chat_context = get_chat_history(user_id, limit=10)

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(f"""
    You are a **friendly and professional mental health assistant**. 
    Always give empathetic, clear, and helpful responses. 

    Example formats:
    - If the user asks for mental health tips, list them clearly.
    - If the user asks about anxiety, explain it in a supportive way.
    - If the user asks an unclear question, ask politely for clarification.

    Here is the recent conversation:
    {chat_context}
    Assistant:
    """,
    generation_config={
        "temperature": 0.7,  # Adjust creativity (lower = more factual, higher = more creative)
        "max_output_tokens": 100,  # Limits response length
    },
    safety_settings=[
        {"category": "HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    ]
)

    # Save Assistant Response to Database
    bot_reply = response.text.strip()
    save_message(user_id, bot_reply, "assistant")

    return jsonify({"response": response.text})  # Gemini's response format

if __name__ == "__main__":
    app.run(debug=True)
