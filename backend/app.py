from flask import Flask
from flask_cors import CORS
from auth import auth_bp
from chatbot import chatbot_bp
from config import DevelopmentConfig
from database import create_tables
from sa import sentiment_bp
from user_profile import profile_bp
from mood import mood_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(sentiment_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(mood_bp)


if __name__ == "__main__":
    create_tables()  # Ensure tables exist before running
    app.run(debug=app.config["DEBUG"])
