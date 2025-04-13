

# **Mentora Frontend**  

This is the **frontend** for **Mentora**, an AI-powered chatbot that provides **sentiment analysis** and **weekly reports with visualizations** based on user conversations. Built using **React.js**.  

---

## **📂 Folder Structure**  
```
/mentora-frontend
│── /components
│   │── Chatbot.js     # Chatbot interface
│   │── Login.js       # Login page
│   │── Signup.js      # Signup page
│── app.js             # Main frontend entry point
│── index.js           # React root file
│── package.json       # Dependencies & scripts
│── README.md          # Project documentation
```

---

## **🚀 Setup Instructions**  

### **1️⃣ Install Dependencies**  
Run the following command inside the frontend folder:  
```bash
npm install
```

### **2️⃣ Start the Development Server**  
```bash
npm start
```
This will start the app on **`http://localhost:3000`**.

---

## **📌 Features**  

✅ **User Authentication** → Login/Signup pages with JWT authentication.  
✅ **Chatbot Interface** → AI-powered chatbot with real-time sentiment tracking.  
✅ **Sentiment Analysis** → Displays mood trends and insights.  
✅ **Weekly Reports** → Users receive **PDF reports** with charts & recommendations.  
✅ **User Profile** → View past sentiment reports & update profile settings.  

---

## **🔗 Navigation Flow**  
| Page        | Path         | Description |
|-------------|-------------|-------------|
| Home        | `/`         | Landing page of Mentora |
| Chatbot     | `/chat`     | Chat interface for conversations |
| Login       | `/login`    | User authentication |
| Signup      | `/signup`   | New user registration |
| Profile     | `/profile`  | View user data & reports |
| Contact Us  | `/contact`  | User support page |

---

## **📌 To-Do**  
- [ ] Enhance chatbot UI for better engagement.  
- [ ] Improve animations & responsiveness for mobile users.  
- [ ] Add a **dark mode toggle** for better accessibility.  
