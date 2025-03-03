
# **Mentora - AI Mental Health Chatbot**  

### **Overview**  
Mentora is an AI-powered mental health support chatbot designed to provide empathetic and professional responses to users seeking mental health guidance. It offers real-time interaction, user authentication, sentiment analysis, and personalized recommendations using the **Google Gemini API**.

---

## **Features**
✅ **User Authentication** (Signup/Login)  
✅ **Chatbot with Short & Long-Term Memory**  
✅ **Sentiment Analysis** for User Conversations  
✅ **Conversation History Storage** (SQLite Database)  
✅ **Flask Backend with React Frontend**  
✅ **Google Gemini AI Integration**  

---

## **Tech Stack**
- **Frontend**: React (Node.js v22.14.0)  
- **Backend**: Flask, Flask-SQLAlchemy, Flask-CORS, Flask-Session  
- **Database**: SQLite (`mentora.db`)  
- **AI Model**: Google Gemini AI API  
- **Authentication**: Secure User Signup/Login  
- **Sentiment Analysis**: Data stored for analysis  

---

## **Installation & Setup**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/Mentora.git
cd Mentora
```

### **2️⃣ Backend Setup**
```sh
cd backend
pip install -r requirements.txt
python app.py
```

### **3️⃣ Frontend Setup**
```sh
cd ../mentora-frontend
npm install
npm start
```

---

## **Database Structure**
📌 **Users Table**: Stores user credentials  
📌 **ChatHistory Table**: Stores chatbot interactions for sentiment analysis  

---

## **API Endpoints**
### **Authentication**
- **`POST /signup`** → Register a new user  
- **`POST /login`** → Authenticate user  

### **Chatbot**
- **`POST /chat`** → Get chatbot response  
- **`GET /history`** → Fetch user chat history  

---

## **How It Works?**
1️⃣ **User signs up/logs in** (stored in SQLite)  
2️⃣ **User interacts with Mentora** (chat stored in DB)  
3️⃣ **Mentora processes response using Google Gemini API**  
4️⃣ **Chat history is analyzed for sentiment trends**  

---

## **Contributing**
Want to contribute? Open an issue or create a pull request! 🎉  

---
