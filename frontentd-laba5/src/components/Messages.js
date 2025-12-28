import React from 'react';

function Messages({ messages }) {
  if (!messages || messages.length === 0) {
    return null;
  }

  return (
    <div className="container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type || 'info'}`}>
            {msg.text}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Messages;