// src/components/FloatingChatbot.jsx
import React, { useState } from 'react';

export default function FloatingChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const toggleChat = () => setIsOpen(!isOpen);

  return (
    <>
      {/* Floating Icon */}
      <div
        onClick={toggleChat}
        style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          backgroundColor: '#4f46e5',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          color: '#fff',
          fontSize: '28px',
          cursor: 'pointer',
          zIndex: 1000,
          boxShadow: '0 8px 24px rgba(79, 70, 229, 0.3), 0 4px 8px rgba(0, 0, 0, 0.1)',
          transition: 'all 0.3s ease',
          border: '2px solid rgba(255, 255, 255, 0.2)',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.1)';
          e.currentTarget.style.boxShadow = '0 12px 32px rgba(79, 70, 229, 0.4), 0 6px 12px rgba(0, 0, 0, 0.15)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
          e.currentTarget.style.boxShadow = '0 8px 24px rgba(79, 70, 229, 0.3), 0 4px 8px rgba(0, 0, 0, 0.1)';
        }}
      >
        💬
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div
          style={{
            position: 'fixed',
            top: '80px', // Below navbar (typically 60px + 20px margin)
            right: '24px',
            width: '400px',
            height: '600px',
            maxHeight: 'calc(100vh - 100px)', // Responsive to viewport
            zIndex: 9999,
            borderRadius: '16px',
            overflow: 'hidden',
            background: '#ffffff',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.15), 0 8px 24px rgba(0, 0, 0, 0.1)',
            border: '1px solid rgba(0, 0, 0, 0.08)',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          {/* Header */}
          <div
            style={{
              backgroundColor: '#4f46e5',
              background: 'linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)',
              color: '#ffffff',
              padding: '16px 20px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontSize: '20px' }}>🤖</span>
              <h3
                style={{
                  margin: 0,
                  fontSize: '16px',
                  fontWeight: '600',
                  letterSpacing: '0.3px',
                }}
              >
                AI Study Assistant
              </h3>
            </div>
            <button
              onClick={toggleChat}
              style={{
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                color: '#ffffff',
                fontSize: '20px',
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                cursor: 'pointer',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                transition: 'all 0.2s ease',
                fontWeight: 'bold',
                lineHeight: '1',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.3)';
                e.currentTarget.style.transform = 'rotate(90deg)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                e.currentTarget.style.transform = 'rotate(0deg)';
              }}
              aria-label="Close chat"
            >
              ✖
            </button>
          </div>

          {/* Chat iframe */}
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <iframe
              src="https://amna-ejaz99-physical-ai-robotics-chatbot.hf.space/"
              style={{
                width: '100%',
                height: '100%',
                border: 'none',
                display: 'block',
              }}
              title="AI Study Assistant Chat"
            />
          </div>
        </div>
      )}

      {/* Mobile Responsive Styles */}
      <style jsx>{`
        @media (max-width: 768px) {
          div[style*="width: 400px"] {
            width: calc(100vw - 32px) !important;
            right: 16px !important;
            left: 16px !important;
            height: calc(100vh - 100px) !important;
            max-height: calc(100vh - 100px) !important;
          }
        }

        @media (max-width: 480px) {
          div[style*="bottom: 24px"] {
            bottom: 16px !important;
            right: 16px !important;
            width: 56px !important;
            height: 56px !important;
            font-size: 26px !important;
          }
        }
      `}</style>
    </>
  );
}




