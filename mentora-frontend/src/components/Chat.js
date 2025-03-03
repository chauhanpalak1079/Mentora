import React, { useState } from "react";

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const sendMessage = async () => {
        if (!input.trim()) return;

        const user_id = localStorage.getItem("user_id");
        if (!user_id) {
            window.location.href = "/login";  // Redirect if not logged in
            return;
        }

        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input, user_id }),
        });

        const data = await response.json();
        setMessages([...messages, { user: input, bot: data.response }]);
        setInput("");
    };

    return (
        <div>
            <h2>Mentora Chatbot</h2>
            <div>
                {messages.map((msg, index) => (
                    <p key={index}>
                        <strong>User:</strong> {msg.user} <br />
                        <strong>Mentora:</strong> {msg.bot}
                    </p>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask something..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default Chat;
