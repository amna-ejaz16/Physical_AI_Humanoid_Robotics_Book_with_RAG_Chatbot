import React, { useState } from "react";

const API_URL =
  "https://amna-ejaz99-physical-ai-robotics-chatbot.hf.space/ask";

export default function FloatingChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const toggleChat = () => setIsOpen(!isOpen);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg.text }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { role: "bot", text: data.answer },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error connecting to server." },
      ]);
    }

    setLoading(false);
  };

  return (
    <>
      {/* Floating Button */}
      <div
        onClick={toggleChat}
        style={{
          position: "fixed",
          bottom: 24,
          right: 24,
          width: 60,
          height: 60,
          borderRadius: "50%",
          background: "#4f46e5",
          color: "#fff",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          fontSize: 26,
          zIndex: 9999,
        }}
      >
        💬
      </div>

      {isOpen && (
        <div
          style={{
            position: "fixed",
            right: 24,
            bottom: 100,
            width: 380,
            height: 520,
            background: "#fff",
            borderRadius: 16,
            display: "flex",
            flexDirection: "column",
            boxShadow: "0 10px 40px rgba(0,0,0,.2)",
            zIndex: 9999,
          }}
        >
          {/* Header */}
          <div
            style={{
              background: "#4f46e5",
              color: "#fff",
              padding: 14,
              fontWeight: "bold",
            }}
          >
            🤖 AI Study Assistant
          </div>

          {/* Messages */}
          <div
            style={{
              flex: 1,
              padding: 12,
              overflowY: "auto",
              fontSize: 14,
            }}
          >
            {messages.map((m, i) => (
              <div key={i} style={{ marginBottom: 8 }}>
                <b>{m.role === "user" ? "You" : "Bot"}:</b> {m.text}
              </div>
            ))}
            {loading && <div>Bot is thinking...</div>}
          </div>

          {/* Input */}
          <div
            style={{
              display: "flex",
              borderTop: "1px solid #ddd",
              padding: 8,
            }}
          >
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your question..."
              style={{
                flex: 1,
                padding: 8,
                border: "1px solid #ccc",
                borderRadius: 6,
              }}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button
              onClick={sendMessage}
              style={{
                marginLeft: 8,
                padding: "8px 14px",
                background: "#4f46e5",
                color: "#fff",
                border: "none",
                borderRadius: 6,
                cursor: "pointer",
              }}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}
