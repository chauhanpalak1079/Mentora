
# **Mentora Backend**  

This is the backend for **Mentora**, a chatbot that provides sentiment analysis on user conversations. The backend handles **user authentication, chatbot responses, sentiment analysis, and database management**.  

## **📂 Folder Structure**  
```
/mentora-backend
│── app.py           # Main backend entry point
│── auth.py          # Handles authentication (JWT-based)
│── chatbot.py       # Chatbot logic and response generation
│── config.py        # Configuration settings (API keys, database paths)
│── database.py      # Database connection and models
│── requirements.txt # List of dependencies
```

---

## **🚀 Setup Instructions**  

### **1️⃣ Install Dependencies**  
Run the following command inside the backend folder:  
```bash
pip install -r requirements.txt
```

### **2️⃣ Run the Backend Server**  
```bash
python app.py
```
This will start the server on **`http://localhost:5000`** (or as specified in `config.py`).

---

## **📌 Features**  

✅ **User Authentication** → JWT-based login/signup (managed in `auth.py`).  
✅ **Chatbot Responses** → AI-powered chatbot using Gemini 1.5 Pro (`chatbot.py`).  
✅ **Sentiment Analysis** → BERT model for mood tracking (`sentiment_analysis.py`).  
✅ **Database Storage** → SQLite (`mentora.db`) to store chat history & reports.  
✅ **PDF Report Generation** → Weekly sentiment analysis reports with charts.  

---

## **🔗 API Endpoints**  

| Method | Endpoint       | Description |
|--------|--------------|-------------|
| POST   | `/login`     | User login (JWT) |
| POST   | `/signup`    | User registration |
| POST   | `/chat`      | Send message & get chatbot response |
| GET    | `/reports`   | Get user sentiment reports |

---

## **📌 To-Do**  
- [ ] Optimize chatbot responses for better engagement.  
- [ ] Improve sentiment analysis accuracy with fine-tuned BERT.  
- [ ] Add a **user dashboard** for interactive reports.  

---

