import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Chat.css";

const Chat = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false); // New state to track Mentora's response
  const navigate = useNavigate();
  const chatEndRef = useRef(null);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  useEffect(() => {
    setTimeout(() => {
      chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory, loading]);

  const fetchChatHistory = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      alert("Unauthorized! Please log in.");
      navigate("/login");
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/chat/history", {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
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
      navigate("/login");
      return;
    }

    const newMessage = { user_message: message, bot_response: null };
    setChatHistory([...chatHistory, newMessage]);
    setMessage("");
    setLoading(true); // Show loading dots

    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    setLoading(false); // Hide loading dots

    if (response.ok) {
      setChatHistory([...chatHistory, { user_message: message, bot_response: data.response }]);
    } else {
      alert(data.error);
    }
  };

  return (
    <div className="chat-container">
      <div className="cloud-background"></div>
      <h2 className="chat-title">Mentora - Mental Health Assistant</h2>
      <div className="chat-box">
        {chatHistory.map((chat, index) => (
          <div key={index} className="chat-message">
            <p className="user-message"><strong>You:</strong> {chat.user_message}</p>
            <p className="mentora-message">
              <strong>Mentora:</strong> {chat.bot_response ? chat.bot_response : ""}
            </p>
          </div>
        ))}

        {loading && (
          <div className="chat-message">
            <p className="mentora-message typing-indicator">
              <strong>Mentora:</strong> <span className="dots">...</span>
            </p>
          </div>
        )}

        <div ref={chatEndRef}></div>
      </div>

      <form onSubmit={sendMessage} className="chat-form">
        <div className="input-container">
          <input 
            type="text" 
            placeholder="Type a message..." 
            value={message} 
            onChange={(e) => setMessage(e.target.value)} 
            required 
            className="chat-input"
          />
          <button type="submit" className="chat-button">Send</button>
        </div>
      </form>
    </div>
  );
};

export default Chat;
