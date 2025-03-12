from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
import jwt  # For JWT authentication
from functools import wraps
from database import get_last_7_days_chat, get_username_by_id  # Removed get_user_password
from config import Config  # Store JWT secret in config.py


# Define Flask Blueprint
sentiment_bp = Blueprint("sentiment", __name__)

# Load Gemini API key
SECRET_KEY = os.getenv("SECRET_KEY", "fucking_do_it_pr0prely") 
genai.configure(api_key=Config.GEMINI_API_KEY)

# JWT Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")  # Get token from headers

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            decoded_token = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])  # Fix Bearer token format
            user_id = decoded_token["user_id"]  # Changed from username to user_id
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(user_id, *args, **kwargs)  # Pass user_id instead of username

    return decorated

# API Route: Analyze Sentiment for a User
@sentiment_bp.route("/analyze_sentiment", methods=["POST"])
@token_required
def analyze_sentiment(user_id):  # Now using user_id
    # Fetch chat history
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404
        
    chat_history = get_last_7_days_chat(username)
    if not chat_history:
        return jsonify({"message": "No chat history found for past 7 days"}), 404

    # Format chat history
    formatted_chat = "\n".join([f"User: {msg} | Bot: {resp}" for msg, resp, _ in chat_history])

    # Define prompt for Gemini API
    prompt = f"""
    Analyze the following 7-day chat history:
    {formatted_chat}

    - Identify emotional trends (happy, sad, anxious, neutral, etc.).
    - Summarize key mood patterns.
    - Provide well-being recommendations based on observed trends.
    """

    # Generate report using Gemini API
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return jsonify({"user_id": user_id, "sentiment_report": response.text})
