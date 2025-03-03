# Components

### **Overview**  
The `components/` folder contains core React components for **Mentora**, handling authentication and chatbot interactions. Dependencies like `axios` are used for API communication.  

---

## **📂 Folder Structure**  
```
mentora-frontend/
│── src/
│   ├── components/
│   │   ├── Chat.js
│   │   ├── Login.js
│   │   ├── Signup.js
│   ├── App.js 
```

---

## **📌 Components Explained**
### **1️⃣ `Login.js`**
🔹 Handles user authentication.  
🔹 Uses `axios` to send login credentials to `/login` API.  
🔹 Saves `user_id` in **localStorage** after successful login.  
🔹 Redirects to `Chat.js`.  

### **2️⃣ `Signup.js`**
🔹 Registers new users.  
🔹 Uses `axios` to send data to `/signup` API.  
🔹 Redirects to `Login.js` after signup.  

### **3️⃣ `Chat.js`**
🔹 Main chatbot interface.  
🔹 Sends user messages to `/chat` API using `axios`.  
🔹 Displays bot responses dynamically.  
🔹 Stores chat history in the **database** for sentiment analysis.  

---

## **⚡ Dependencies & Installation**
**Required Packages:**
```sh
npm install axios react-router-dom
```
🔹 **axios** → Handles API requests (`/login`, `/signup`, `/chat`).  
🔹 **react-router-dom** → Enables navigation between Login, Signup, and Chat pages.  

---

## **🚀 How Components Work Together**
1️⃣ **User visits Login/Signup page**  
2️⃣ **On login, session is stored, user is redirected to Chat.js**  
3️⃣ **Chat.js sends user input to Flask backend, receives response**  
4️⃣ **Chat history is displayed dynamically**  

---

## **⚙️ Setup Instructions**
1️⃣ **Ensure Node.js v22.14.0 is installed**  
2️⃣ **Install dependencies**
```sh
npm install
```
3️⃣ **Run the frontend**
```sh
npm start
```

---

