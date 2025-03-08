import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fucking_do_it_pr0prely")  # Change this in production
    SESSION_TYPE = "filesystem"  # Session storage type
    DATABASE_NAME = "mentora.db"  # SQLite database
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBcfVY6OI_pQdROE-CCgMb1hLgKXukWya0")  # Gemini API key

class DevelopmentConfig(Config):
    DEBUG = True  # Enable debugging

class ProductionConfig(Config):
    DEBUG = False  # Disable debugging





    