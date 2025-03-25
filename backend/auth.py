from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

import jwt
import datetime
import bcrypt
from flask import Flask, request, jsonify
from database import get_db_connection, add_user  # Import database connection

app = Flask(__name__)
a="fucking_do_it_pr0prely"
SECRET_KEY = a  # Use environment variables in production


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    password = data.get('password')

    # Validation: Ensure all fields are present
    if not all([username, first_name, last_name, dob, password]):
        return jsonify({"error": "All fields are required"}), 400

    success = add_user(username, first_name, last_name, dob, password)

    if not success:
        return jsonify({"error": "Username already exists"}), 409  

    # ✅ Generate JWT Token upon successful signup
    token_payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Token valid for 7 days
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "User registered successfully!", "token": token}), 201



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

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):  # FIXED: Ensure correct encoding
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


def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f"✅ Decoded JWT: {payload}")  # Debugging output
        return payload.get("user_id")  # Ensure 'user_id' is inside the token
    except jwt.ExpiredSignatureError:
        print("❌ Token expired")
        return None
    except jwt.InvalidTokenError:
        print("❌ Invalid token")
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
