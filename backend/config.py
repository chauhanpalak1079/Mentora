import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "create a key for urself")  # Change this in production
    SESSION_TYPE = "filesystem"  # Session storage type
    DATABASE_NAME = "mentora.db"  # SQLite database
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "enter ur api key here")  # Gemini API key

class DevelopmentConfig(Config):
    DEBUG = True  # Enable debugging

class ProductionConfig(Config):
    DEBUG = False  # Disable debugging





    
