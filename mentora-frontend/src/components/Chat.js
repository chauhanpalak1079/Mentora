import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Chat.css";

const Chat = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const chatEndRef = useRef(null);

  useEffect(() => {
    fetchChatHistory();
    // Start emotion detection when the component mounts
    startEmotionDetection();

    return () => {
      // Stop emotion detection when the component unmounts
      stopEmotionDetection();
    };
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
    setLoading(true);

    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    setLoading(false);

    if (response.ok) {
      setChatHistory([...chatHistory, { user_message: message, bot_response: data.response }]);
    } else {
      alert(data.error);
    }
  };

  // Function to start emotion detection
  const startEmotionDetection = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      alert("Unauthorized! Please log in.");
      navigate("/login");
      return;
    }

    // Make an API request to start emotion detection
    const data = {};  // Ensure this is an object, even if empty
    const response = await fetch("http://127.0.0.1:5000/start-camera", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data), // Ensure this is correctly formatted
});

    if (!response.ok) {
      alert("response error");
}
  };

  // Function to stop emotion detection
  const stopEmotionDetection = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      alert("Unauthorized! Please log in.");
      navigate("/login");
      return;
    }

    // Make an API request to stop emotion detection
    const response = await fetch("http://127.0.0.1:5000/stop-camera", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      alert("Failed to stop emotion detection.");
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
              <strong></strong> <span className="dots"></span>
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

          {/* Send Button */}
          <button type="submit" className="chat-button">Send</button>
        </div>
      </form>
    </div>
  );
};

export default Chat;
