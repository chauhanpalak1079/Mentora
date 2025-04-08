import os
import torch
import cv2
import numpy as np
from PIL import Image
import threading
import time
import google.generativeai as genai
from flask import Blueprint, request, jsonify
from database import get_db_connection, fetch_chat_history, get_user_name, get_username_by_id, get_emotion_db_connection
from config import Config
from auth import verify_jwt
from util import *

chatbot_bp = Blueprint("chatbot", __name__)
genai.configure(api_key=Config.GEMINI_API_KEY)

# Check if CUDA is available
use_cuda = torch.cuda.is_available()
device = 'cuda' if use_cuda else 'cpu'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
weights_dir = os.path.join(BASE_DIR, "weights")

# Ensure weights exist
if not os.path.exists(weights_dir):
    raise FileNotFoundError(f"Weights folder not found: {weights_dir}")

detection_model_path = os.path.join(weights_dir, "detection.onnx")
emotion_model_path = os.path.join(weights_dir, "emotion.onnx")

if not os.path.exists(detection_model_path) or not os.path.exists(emotion_model_path):
    raise FileNotFoundError("Model weights not found in weights directory.")

# Load models
detector = FaceDetector(detection_model_path)
fer = HSEmotionRecognizer(emotion_model_path)

# Emotion storage
emotion_scores = {
    "anger": [],
    "disgust": [],
    "fear": [],
    "happiness": [],
    "neutral": [],
    "sadness": [],
    "surprise": []
}

is_running = False  
capture_thread = None


def detect_face(frame):
    boxes = detector.detect(frame, (640, 640))
    return boxes if boxes is not None and len(boxes) else None


def capture_emotions(username):
    global is_running, emotion_scores
    is_running = True
    stream = cv2.VideoCapture(0)  

    while is_running:
        ret, frame = stream.read()
        if not ret:
            print("Error: Camera not available")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = detect_face(image)

        if boxes is not None:
            for box in boxes.astype('int32'):
                x1, y1, x2, y2 = box[:4]
                face_image = image[y1:y2, x1:x2]
                pil_image = Image.fromarray(face_image).convert('RGB')
                pil_image = pil_image.resize((224, 224))  

                emotion, scores = fer.predict_emotions(np.array(pil_image), logits=False)

                for i, emo in enumerate(["anger", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]):
                    emotion_scores[emo].append(scores[i])

        time.sleep(0.1)

    stream.release()
    cv2.destroyAllWindows()
    save_emotions_to_db(username)


def save_emotions_to_db(username):
    conn = get_emotion_db_connection()
    cursor = conn.cursor()

    avg_scores = {emo: (sum(scores) / len(scores)) if scores else 0 for emo, scores in emotion_scores.items()}
    avg_scores = {emotion: score * 100 for emotion, score in avg_scores.items()}
    avg_scores = {key: float(value) for key, value in avg_scores.items()}
    print(avg_scores)
    cursor.execute("""
        INSERT INTO emotions (username, anger, disgust, fear, happiness, neutral, sadness, surprise)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, avg_scores["anger"], avg_scores["disgust"], avg_scores["fear"], avg_scores["happiness"], 
          avg_scores["neutral"], avg_scores["sadness"], avg_scores["surprise"]))

    conn.commit()
    conn.close()

    for emo in emotion_scores:
        emotion_scores[emo] = []

@chatbot_bp.route('/start-camera', methods=['POST'])
def start_camera():
    global capture_thread, is_running
    if 'application/json' not in request.content_type:
        return jsonify({"error": "Unsupported Media Type. Expected application/json"}), 415

    try:
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        user_id = verify_jwt(token.split(" ")[1])
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        username = get_username_by_id(user_id)
    
        if not is_running:
            print("Starting emotion detection thread...")
            capture_thread = threading.Thread(target=capture_emotions, args=(username,))
            capture_thread.start()
            return jsonify({"message": "Camera started for emotion detection."}), 200
        return jsonify({"message": "Emotion detection is already running."}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to start camera: {str(e)}"}), 500


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    global capture_thread, is_running

    data = request.json
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    user_id = verify_jwt(token.split(" ")[1])
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    message = data.get('message')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    username = get_username_by_id(user_id)
    
    print(username)

    if not is_running:
        capture_thread = threading.Thread(target=capture_emotions, args=(username,))
        capture_thread.start()

    r = generate_response(username, message)
    bot_response = r.strip()

    cursor.execute("INSERT INTO chat_history (username, user_message, bot_response) VALUES (?, ?, ?)", 
                   (username, message, bot_response))
    conn.commit()
    conn.close()
      
    return jsonify({"response": bot_response})


@chatbot_bp.route('/chat/history', methods=['GET'])
def get_chat_history():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    user_id = verify_jwt(token.split(" ")[1])
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    username = get_username_by_id(user_id)

    cursor.execute("SELECT user_message, bot_response, timestamp FROM chat_history WHERE username = ? ORDER BY timestamp ASC", (username,))
    chat_logs = cursor.fetchall()
    conn.close()
    print("Fetched history from DB:", chat_logs)
    
    return jsonify({
        "history": [
            {"user_message": log[0], "bot_response": log[1], "timestamp": log[2]} for log in chat_logs
        ]
    })


@chatbot_bp.route('/stop-camera', methods=['POST'])
def stop_emotion():
    global is_running
    is_running = False
    return jsonify({"message": "Emotion detection stopped"}), 200


def generate_response(username, message):
    user_name = get_user_name(username)
    greeting = f"Hello {user_name}," if user_name else "Hello,"

    chat_history = fetch_chat_history(username, limit=5)

    formatted_history = "\n".join([
        f"User: {msg['user_message']}\nAssistant: {msg['bot_response']}" for msg in chat_history
    ])

    prompt = f"""
    You are **Mentora**, a Mood Journal Assistant and Meditation Coach.
    Your job is to help users reflect on emotions and provide relaxation exercises.

    {greeting} Here’s the past conversation:
    {formatted_history}

    Now, continue the conversation:
    User: {message}
    Assistant:
    """

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt, generation_config={"temperature": 0.7, "max_output_tokens": 300})

    return response.text
