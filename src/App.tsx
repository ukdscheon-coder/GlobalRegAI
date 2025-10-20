import React, { useState } from 'react';
import axios from 'axios';
import './index.css';
import { SearchInput } from './components/SearchInput';
import { ChatHistory } from './components/ChatHistory';

export interface Message {
  sender: 'user' | 'ai';
  text: string;
  sources?: { source: string, page: number | string }[];
}

const BACKEND_URL = 'https://globalregai-backend-wcsg33p67a-an.a.run.app/query';
function App() {
  const [chatHistory, setChatHistory] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (userInput: string) => {
    if (!userInput.trim()) return;
    const userMessage: Message = { sender: 'user', text: userInput };
    setChatHistory(prev => [...prev, userMessage]);
    setIsLoading(true);

    if (!BACKEND_URL) {
      const errorMessage: Message = { sender: 'ai', text: '오류: 백엔드 서버 주소가 설정되지 않았습니다. Vercel 환경 변수를 확인해주세요.' };
      setChatHistory(prev => [...prev, errorMessage]);
      setIsLoading(false);
      return;
    }

    try {
      const response = await axios.post(BACKEND_URL, {
        question: userInput
      });
      const aiMessage: Message = {
        sender: 'ai',
        text: response.data.answer,
        sources: response.data.sources
      };
      setChatHistory(prev => [...prev, aiMessage]);

    } catch (error) {
      let errorMessageText = '답변을 생성하는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
      if (axios.isAxiosError(error) && error.response) {
        errorMessageText = `서버 오류: ${error.response.data.error || error.message}`;
      } else if (axios.isAxiosError(error)) {
        errorMessageText = `네트워크 오류: ${error.message}. 백엔드 서버가 정상적으로 실행 중인지 확인해주세요.`;
      }
      const errorMessageObj: Message = { sender: 'ai', text: errorMessageText };
      setChatHistory(prev => [...prev, errorMessageObj]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>GlobalRegAI 🚀</h1>
        <p>AI 기반 글로벌 규제 의사결정 시스템</p>
      </header>
      <ChatHistory chatHistory={chatHistory} isLoading={isLoading} />
      <SearchInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}

export default App;