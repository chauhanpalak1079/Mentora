import sqlite3
from datetime import datetime, timedelta
from collections import Counter
import bcrypt

DATABASE_NAME = "mentora.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enables dictionary-style row access
    return conn
import sqlite3



def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            dob TEXT,
            gender TEXT,
            password TEXT NOT NULL
        )
    ''')
    

    # Chat History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    """)
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sentiment_score REAL NOT NULL,
            sentiment_label TEXT NOT NULL
        )
    ''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS mood_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    date DATE NOT NULL,
    mood TEXT NOT NULL,
    influence TEXT NOT NULL,
    sleep_quality TEXT NOT NULL,
    food_intake TEXT NOT NULL,
    coping_mechanism TEXT NOT NULL,
    improvement_goal TEXT NOT NULL,
    note TEXT,
    UNIQUE(username, date)
)
''')

    conn.commit()
    conn.close()

def get_user_profile(username):
    conn = sqlite3.connect('mentora.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, first_name, last_name,email, gender, dob 
        FROM users WHERE username=?
    """, (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'username': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'email' : row[3],
            'gender' : row[4],
            'dob': row[5]
        }
    return None


def add_user(username, first_name, last_name, email, dob, gender,  password):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cursor.execute("INSERT INTO users (username, first_name, last_name, email, dob, gender,  password) VALUES (?, ?, ?, ? , ? ,?, ?)", 
                       (username, first_name, last_name, email, dob, gender, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user



def get_user_name(username):
    """Fetch the user's real name from the database using their username."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT first_name FROM users WHERE username=?", (username,))
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

def get_last_7_days_chat(username):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    # Get timestamp for 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

    # SQL query to fetch last 7 days of chat history
    cursor.execute("""
        SELECT user_message, bot_response, timestamp 
        FROM chat_history 
        WHERE username = ? AND timestamp >= ?
        ORDER BY timestamp ASC;
    """, (username, seven_days_ago))

    chat_history = cursor.fetchall()  # Fetch data
    conn.close()

    return chat_history  # Returns list of (user_message, bot_response, timestamp)

def get_user_password(username):
    """Fetch the hashed password of a user from the database."""
    conn = sqlite3.connect("mentora.db")  
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None  # Return password if found, else None


def get_username_by_id(user_id):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else None



def save_sentiment_report(user_id, username, sentiment_score, sentiment_label):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO sentiment_reports (user_id, username, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, sentiment_score, sentiment_label))

    conn.commit()
    conn.close()


def get_sentiment_scores(username):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()
    
    query = """
    SELECT report_date, sentiment_score 
    FROM sentiment_reports 
    WHERE username = ? 
    AND report_date >= datetime('now', '-7 days')
    ORDER BY report_date ASC;
    """
    
    cursor.execute(query, (username,))
    data = cursor.fetchall()
    
    conn.close()
    
    # Convert list of tuples to dictionary {date: score}
    sentiment_dict = {row[0]: row[1] for row in data}
    
    return sentiment_dict

def get_latest_sentiment(username):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sentiment_score, sentiment_label 
        FROM sentiment_reports 
        WHERE username = ? 
        ORDER BY report_date DESC 
        LIMIT 1
    """, (username,))

    latest_sentiment = cursor.fetchone()
    conn.close()

    return latest_sentiment

def get_last_7_days_sentiments(username):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sentiment_label 
        FROM sentiment_reports 
        WHERE username = ? 
        AND report_date >= datetime('now', '-7 days')
        ORDER BY report_date DESC
    """, (username,))

    sentiments = [row[0] for row in cursor.fetchall()]
    conn.close()

    return sentiments

def get_sleep_quality_data(username):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    query = """
    SELECT date, sleep_quality
    FROM mood_logs
    WHERE username = ?
    ORDER BY date DESC
    LIMIT 7;
    """

    cursor.execute(query, (username,))
    data = cursor.fetchall()
    conn.close()

    # Reverse to maintain chronological order (oldest first)
    sleep_data = {row[0]: row[1] for row in reversed(data) if row[1] is not None}

    return sleep_data

def get_last_7_mood_entries(username):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    query = """
    SELECT date, mood 
    FROM mood_logs 
    WHERE username = ? 
    ORDER BY date DESC 
    LIMIT 7;
    """
    cursor.execute(query, (username,))
    results = cursor.fetchall()
    conn.close()

    # returns list of tuples like: [('2025-04-07', 'Happy'), ...]
    return results

import sqlite3
from datetime import datetime

def get_logged_dates_for_month(username):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    # Get the current year and month
    now = datetime.now()
    year_month = now.strftime('%Y-%m')

    query = """
    SELECT date 
    FROM mood_logs 
    WHERE username = ? AND strftime('%Y-%m', date) = ?
    """
    cursor.execute(query, (username, year_month))
    rows = cursor.fetchall()
    conn.close()

    # Return list of logged dates like ['2025-04-01', '2025-04-02']
    return [row[0] for row in rows]

def get_coping_mechanism_data(username):
    conn = sqlite3.connect("mentora.db")
    cursor = conn.cursor()

    query = """
    SELECT coping_mechanism
    FROM mood_logs
    WHERE username = ?
    AND date >= date('now', '-30 days')
    """
    cursor.execute(query, (username,))
    rows = cursor.fetchall()
    conn.close()

    mechanisms = []
    for (entry,) in rows:
        if entry:
            mechanisms.extend([m.strip().capitalize() for m in entry.split(',')])
    return mechanisms


def get_emotion_db_connection():
    conn = sqlite3.connect("emotion_data.db")  # Use absolute path
    conn.row_factory = sqlite3.Row
    return conn

def create_emotion_table():
    conn = get_emotion_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS emotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    happiness REAL,
    neutral REAL,
    sadness REAL,
    anger REAL,
    surprise REAL,
    fear REAL,
    disgust REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

    conn.commit()
    conn.close()

def get_latest_emotion_record(username):
    conn = get_emotion_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT happiness, neutral, sadness, anger, surprise, fear, disgust
        FROM emotions
        WHERE username = ?
        ORDER BY timestamp DESC LIMIT 1
    """, (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result  # returns a tuple (happiness, neutral, sadness, anger, surprise, fear, disgust)
    return None


# Run this script once to create tables
if __name__ == "__main__":
    create_tables()
    create_emotion_table()
    print("Database tables created successfully.")
