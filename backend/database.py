import sqlite3

DATABASE_NAME = "mentora.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Enables dictionary-style row access
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # User Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Chat History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()

def get_user_name(username):
    """Fetch the user's real name from the database using their username."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    
    conn.close()
    
    return row[0] if row else None  # Return name if found, else None

def fetch_chat_history(username, limit=5):
    """Fetch the last few messages from the chat history of a user."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_message, bot_response FROM chat_history WHERE username=? ORDER BY timestamp DESC LIMIT ?", 
                   (username, limit))
    rows = cursor.fetchall()
    
    conn.close()

    return [{"user_message": row[0], "bot_response": row[1]} for row in rows]

def store_chat_message(username, user_message, bot_response):
    """Store user and bot messages in the chat history table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO chat_history (username, user_message, bot_response, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", 
                   (username, user_message, bot_response))
    
    conn.commit()
    conn.close()


# Run this script once to create tables
if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")


