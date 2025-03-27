import sqlite3

conn = sqlite3.connect("mentora.db")
cursor = conn.cursor()

user_id = 1  # Replace with the user_id that failed
cursor.execute("SELECT * FROM chat_history ")
user = cursor.fetchall()

print("🔍 User in DB:", user)
conn.close()

#this is only a test file, you can delete it
