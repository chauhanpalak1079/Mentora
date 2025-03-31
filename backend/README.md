# Backend Python files Overview

The Mentora backend is responsible for handling user authentication, chatbot logic, sentiment analysis, and real-time emotion detection. It is built using Flask and interacts with an SQLite database (mentora.db) for storing user data, chat history, and sentiment reports.

**🔹 Key Components of Mentora Backend**


1️⃣ Authentication (auth.py)

Implements JWT authentication for secure login and session management.

Handles user registration, login, and token verification.


2️⃣ Chatbot Logic (chatbot.py)

Uses the Gemini 1.5 Pro API to generate chatbot responses.

Stores user messages and bot replies in the chat_history table.

Integrates real-time emotion detection to analyze user emotions during chat.


3️⃣ Database Management (database.py)

Manages all interactions with SQLite (mentora.db).

Stores user details, chat history, and weekly sentiment reports.

Includes functions to fetch chat history, store sentiment scores, and generate reports.


4️⃣ Sentiment Analysis (sentimental_analysis.py)

Uses BERT (nlptown/bert-base-multilingual-uncased-sentiment) for mood detection.

Analyzes the past 7 days of messages to generate weekly reports.

Integrates with Gemini API for generating report summaries.


5️⃣ Real-Time Emotion Detection (real_time_emotion.py)

Uses a pre-trained CNN model to recognize facial emotions from the webcam.

Runs in the background and records average emotion scores during chat sessions.

Stores session-based emotion data in a separate SQLite database (emotion_data.db).


6️⃣ API Endpoints (app.py)

Provides various API routes for:

✅ User authentication (/login, /register)

✅ Chatbot interaction (/chat)

✅ Sentiment analysis (/analyze-sentiment)

✅ Starting/stopping real-time emotion detection (/start-emotion, /stop-emotion)


**🔹 How Mentora Backend Works**

1️⃣ User logs in → Authenticated via JWT.

2️⃣ User starts chatting → Chatbot processes input using Gemini API.

3️⃣ Real-time emotion detection → Records facial expressions during chat.

4️⃣ Data is stored → Chat logs go into mentora.db, emotions into emotion_data.db.

5️⃣ Sentiment reports are generated → Weekly mood trends & visualizations.

**🔹 Technologies Used**

✔ Flask (Backend framework)

✔ SQLite (Database)

✔ JWT (Authentication)

✔ Gemini API (Chatbot + Reports)

✔ BERT (Sentiment Analysis)

✔ Pretrained CNN (Emotion detection)



This backend ensures smooth integration between chatbot interactions, sentiment analysis, and emotion tracking while keeping the system secure, efficient, and scalable. 🚀

