import React, { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const res = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });

    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Mentora Chatbot</h2>
      <input 
        type="text" 
        value={input} 
        onChange={(e) => setInput(e.target.value)} 
        placeholder="Ask something..." 
        style={{ padding: "10px", width: "60%" }} 
      />
      <button onClick={handleSend} style={{ padding: "10px", marginLeft: "10px" }}>
        Send
      </button>
      <p><strong>Response:</strong> {response}</p>
    </div>
  );
}

export default App;
