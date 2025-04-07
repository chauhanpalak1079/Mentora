from flask import Blueprint, request, jsonify
import sqlite3
import jwt, os
from datetime import date, datetime
from functools import wraps
from database import get_username_by_id

mood_bp = Blueprint("mood",__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "///")  # Replace with your actual key

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


# --- POST: Log Mood (once per day) ---
@mood_bp.route('/mood-log', methods=['POST'])
@token_required
def log_mood(user_id):
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    selected_date = data.get("date") or date.today().isoformat()
    # Check if the date is in the future
    if datetime.fromisoformat(selected_date).date() > date.today():
        return jsonify({"message": "You cannot log mood for future dates."}), 400
    # Extract fields
    mood = data.get('mood')
    influence = data.get('influence')
    sleep = data.get('sleep_quality')
    food = data.get('food_intake')
    coping = data.get('coping_mechanism')
    improve = data.get('improvement_goal')
    note = data.get('note', '')

    if not all([mood, influence, sleep, food, coping, improve]):
        return jsonify({"message": "Missing required fields"}), 400

    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    # Check if entry already exists for that date
    cursor.execute("SELECT * FROM mood_logs WHERE username = ? AND date = ?", (username, selected_date))
    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "Mood already logged for this date."}), 400

    # Insert new mood log
    cursor.execute('''
        INSERT INTO mood_logs (
            username, date, mood, influence, sleep_quality,
            food_intake, coping_mechanism, improvement_goal, note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, selected_date, mood, influence, sleep, food, coping, improve, note))

    conn.commit()
    conn.close()
    return jsonify({"message": "Mood entry logged successfully."}), 201

# --- GET: All logged dates ---
@mood_bp.route('/mood-log/dates', methods=['GET'])
@token_required
def get_logged_dates(user_id):
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404

    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date FROM mood_logs WHERE username = ?
    ''', (username,))
    rows = cursor.fetchall()
    conn.close()

    logged_dates = [row[0] for row in rows]
    return jsonify({"logged_dates": logged_dates})

# --- GET: Mood log for specific date ---
@mood_bp.route('/mood-log/<selected_date>', methods=['GET'])
@token_required
def get_mood_log_by_date(user_id, selected_date):
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404

    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT mood, influence, sleep_quality, food_intake,
               coping_mechanism, improvement_goal, note
        FROM mood_logs
        WHERE username = ? AND date = ?
    ''', (username, selected_date))

    row = cursor.fetchone()
    conn.close()

    if row:
        keys = ["mood", "influence", "sleep_quality", "food_intake", "coping_mechanism", "improvement_goal", "note"]
        result = dict(zip(keys, row))
        return jsonify(result)
    else:
        return jsonify({"message": "No mood log found for this date."}), 404
