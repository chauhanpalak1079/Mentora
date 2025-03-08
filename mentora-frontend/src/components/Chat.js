import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom"; // ✅ React Router for navigation

const Chat = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const navigate = useNavigate(); // ✅ Use navigate for redirection
  const chatEndRef = useRef(null); 

  useEffect(() => {
    fetchChatHistory(); // Load chat history on page load
  }, []);


  useEffect(() => {
    // Scroll to bottom when the component loads
    setTimeout(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100); // Small delay ensures chat renders before scrolling
  }, []); // Runs only on page load

  useEffect(() => {
    // Scroll to bottom whenever messages update
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [message]);


  const fetchChatHistory = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      alert("Unauthorized! Please log in.");
      navigate("/login"); // ✅ Redirect to login if no token
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/chat/history", {
      method: "GET",
      headers: { "Authorization": `Bearer ${token}` },
    });

    const data = await response.json();

    if (response.ok) {
      setChatHistory(data.history);
    } else {
      alert(data.error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");

    if (!token) {
      alert("Unauthorized! Please log in.");
      navigate("/login"); // ✅ Redirect to login if not authenticated
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();

    if (response.ok) {
      setChatHistory([...chatHistory, { user_message: message, bot_response: data.response }]);
      setMessage("");
    } else {
      alert(data.error);
    }
  };

  return (
    <div>
      <h2>Mentora - Mental Health Assistant</h2>
      <div>
        {chatHistory.map((chat, index) => (
          <div key={index}>
            <p><strong>You:</strong> {chat.user_message}</p>
            <p><strong>Mentora:</strong> {chat.bot_response}</p>
          </div>
        ))}
      </div>
    <div ref={chatEndRef}>
    <form onSubmit={sendMessage}>
        <input type="text" placeholder="Type a message..." value={message} onChange={(e) => setMessage(e.target.value)} required />
        <button type="submit">Send</button>
      </form>
    </div>
    </div>
  );
};

export default Chat;
