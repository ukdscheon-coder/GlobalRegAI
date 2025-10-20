import React, { useState } from 'react';

interface Props {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export const SearchInput: React.FC<Props> = ({ onSendMessage, isLoading }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <form className="search-input-container" onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="AI 규제 전문가에게 질문하세요..."
        disabled={isLoading}
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? '...' : '전송'}
      </button>
    </form>
  );
};