# **Mentora Backend**  

This is the backend for **Mentora**, a mental health chatbot built using Flask, SQLite, and the Google Gemini AI API. The backend handles user authentication, chatbot responses, and conversation storage for sentiment analysis.  

## **Tech Stack**  
- **Backend:** Flask (Python)  
- **Database:** SQLite (Flask-SQLAlchemy)  
- **Authentication:** Flask-Session, Werkzeug  
- **AI Model:** Google Gemini API  

---

## **Installation Guide**  

### **1. Clone the Repository**  
```sh
git clone https://github.com/your-repo/Mentora.git
cd Mentora/backend
```

### **2. Create a Virtual Environment (Optional but Recommended)**  
```sh
python -m venv venv  
source venv/bin/activate  # Mac/Linux  
venv\Scripts\activate  # Windows  
```

### **3. Install Dependencies**  
```sh
pip install -r requirements.txt
```

---

## **Environment Variables**  
Create a **`.env`** file in the backend folder and add your **Google Gemini API key**:  
```
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

---

## **Database Setup**  

The backend uses **SQLite** to store user data and chat history. Run the following command to create the database:  
```sh
python setup_db.py
```

---

## **Running the Backend**  

Start the Flask server using:  
```sh
python app.py
```
The server will run on **`http://127.0.0.1:5000/`**.

---

## **API Endpoints**  

### **1. User Authentication**  
| Method | Endpoint       | Description |
|--------|--------------|-------------|
| `POST` | `/signup`     | Registers a new user |
| `POST` | `/login`      | Authenticates user & returns session token |
| `POST` | `/logout`     | Logs out the user |

### **2. Chatbot API**  
| Method | Endpoint  | Description |
|--------|-----------|-------------|
| `POST` | `/chat`   | Sends a message & gets AI-generated response |

---

## **`requirements.txt`**  

```
flask==3.0.0
flask-cors==4.0.0
flask-session==0.4.0
flask-sqlalchemy==3.1.1
werkzeug==3.0.1
google-generativeai==0.4.0
requests==2.31.0
python-dotenv==1.0.0
```

---

## **Troubleshooting**  

### 🔹 **Module Not Found?**  
Run:  
```sh
pip install -r requirements.txt
```

### 🔹 **Server Not Starting?**  
Check if **port 5000** is busy:  
```sh
lsof -i :5000  # Mac/Linux  
netstat -ano | findstr :5000  # Windows  
```
Kill the process using:  
```sh
kill -9 <PID>  # Mac/Linux  
taskkill /PID <PID> /F  # Windows  
```

---

## **Contributing**  
Feel free to submit **issues** or **pull requests**! 🎯  

---


