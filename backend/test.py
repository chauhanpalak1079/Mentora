import sqlite3
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect("mentora.db")
cursor = conn.cursor()
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

    return chat_history

chat_history = get_last_7_days_chat("kauss")

print(chat_history)
# Close the connection
conn.close()

