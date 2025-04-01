# 📂 Mentora Frontend - `components/` Folder  

The `components/` folder contains all **React components** that power the user interface of Mentora. Each component plays a role in handling **authentication, chatbot interactions, sentiment analysis, and mood tracking**.  

---

## 📌 **Key Components**  

### **1️⃣ `signup.js` - User Signup Page**  
🔹 Provides a **signup form** for new users.  
🔹 Sends user details to the backend (`/register` API).  
🔹 Handles **error messages** for invalid input.  

### **2️⃣ `login.js` - User Login Page**  
🔹 Allows users to log in with their **email and password**.  
🔹 Authenticates users via **JWT tokens**.  
🔹 Redirects users to the **chat page** after successful login.  

### **3️⃣ `chatbot.js` - Chatbot Interface**  
🔹 The **main chat page** where users interact with the chatbot.  
🔹 Sends user messages to the backend (`/chat` API) and displays bot responses.  
🔹 Triggers **real-time emotion detection** in the background.  
🔹 Emotion detection **runs in the backend** (no frontend preview).  

### **4️⃣ `sentimentReport.js` - Sentiment Analysis Reports**  
🔹 Fetches and displays **weekly sentiment reports** from the backend.  
🔹 Shows **charts and graphs** (e.g., mood trends, pie charts, line graphs).  
🔹 Allows users to view **past sentiment reports**.  

---

## ⚡ **How the `components/` Folder Works**  
✅ **React-based UI** for smooth user experience.  
✅ Communicates with **Flask backend** via **API requests**.  
✅ Uses **JWT for authentication** and **stores user sessions**.  
✅ Integrates with **sentiment analysis and chatbot features**.  

This structure ensures a **modular and maintainable frontend** for Mentora. 🚀  

