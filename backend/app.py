from flask import Flask
from flask_cors import CORS
from flask_session import Session
from auth import auth_bp
from chatbot import chatbot_bp
from config import DevelopmentConfig
from database import create_tables

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
Session(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(chatbot_bp)

if __name__ == "__main__":
    create_tables()  # Ensure tables exist before running
    app.run(debug=app.config["DEBUG"])
