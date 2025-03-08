from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

import jwt
import datetime
import bcrypt
from flask import Flask, request, jsonify
from database import get_db_connection  # Import database connection

app = Flask(__name__)
a="paksdjfjidodmcvn"
SECRET_KEY = a  # Use environment variables in production

# 🔹 User Signup API
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    name = data.get('name')
    password = data.get('password')

    if not username or not name or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, name, password) VALUES (?, ?, ?)", 
                   (username, name, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully!"}), 201

# 🔹 User Login API (Generates JWT)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
        token = jwt.encode(
            {"user_id": user[0], "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

# 🔹 JWT Verification Middleware
def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# 🔹 Protected Route Example
@auth_bp.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token missing"}), 401

    user_id = verify_jwt(token.split(" ")[1])  # Remove 'Bearer ' prefix
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    return jsonify({"message": "Welcome!", "user_id": user_id})

if __name__ == '__main__':
    app.run(debug=True)
