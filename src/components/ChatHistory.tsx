import React from 'react';
import { Message } from '../App';

interface Props {
  chatHistory: Message[];
  isLoading: boolean;
}

export const ChatHistory: React.FC<Props> = ({ chatHistory, isLoading }) => {
  return (
    <div className="chat-history">
      {chatHistory.map((msg, index) => (
        <div key={index} className={`chat-message ${msg.sender}`}>
          <div className="message-bubble">
            <p style={{ margin: 0 }}>{msg.text}</p>
            {msg.sender === 'ai' && msg.sources && msg.sources.length > 0 && (
              <div className="sources-container">
                <strong>[근거 자료]</strong>
                <ul>
                  {msg.sources.map((src, idx) => (
                    <li key={idx}>
                      {src.source} (페이지: {src.page})
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      ))}
      {isLoading && (
        <div className="chat-message ai">
          <div className="message-bubble">
            <div className="loading-spinner"></div>
          </div>
        </div>
      )}
    </div>
  );
};