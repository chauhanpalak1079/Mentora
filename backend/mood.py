from flask import Blueprint, request, jsonify
import sqlite3
import jwt, os
from functools import wraps
from database import get_username_by_id

mood_bp = Blueprint("mood",__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "fucking_do_it_pr0prely")  # Replace with your actual key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data['user_id']
        except Exception as e:
            print("❌ JWT decode failed:", str(e))
            return jsonify({'message': f'Token is invalid: {str(e)}'}), 401
        return f(user_id, *args, **kwargs)
    return decorated


# --- Mood Logging API ---
@mood_bp.route('/mood-log', methods=['POST'])
@token_required
def log_mood(user_id):
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()

    mood = data.get('mood')
    influence = data.get('influence')
    improve_action = data.get('improve_action')
    note = data.get('note', '')  # optional field

    if not all([mood, influence, improve_action]):
        return jsonify({"message": "Missing required fields"}), 400

    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO mood_logs (username, mood, influence, improve_action, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, mood, influence, improve_action, note))

    conn.commit()
    conn.close()
    print ("done")
    return jsonify({"message": "Mood entry logged successfully."}), 201
