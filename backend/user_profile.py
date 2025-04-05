from flask import Blueprint, jsonify, request
from database import get_user_profile, get_username_by_id
import os
from functools import wraps
import jwt

profile_bp = Blueprint('profile', __name__)
SECRET_KEY = os.getenv("SECRET_KEY", "fucking_do_it_pr0prely") 

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            decoded_token = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(user_id, *args, **kwargs)

    return decorated


@profile_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(user_id):
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404

    user_data = get_user_profile(username)
    if user_data:
        return jsonify({
            'username': user_data['username'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'dob': user_data['dob']
        }), 200
    return jsonify({'message': 'User not found'}), 404
