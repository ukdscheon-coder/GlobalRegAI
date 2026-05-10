import { useState } from 'react';
import { Send, Settings, Database, Activity, Map } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([{ role: 'system', content: 'Welcome to GlobalRegAI. How can I assist you with regulatory affairs today?' }]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      // Connect to local Ollama API
      const response = await fetch('http://localhost:11434/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'llama3', // or 'mistral', 'llama2'
          prompt: input,
          system: "You are GlobalRegAI, an expert in Medical Device, Pharma, Cosmetics, and Food Regulatory Affairs (FDA, EMA, MFDS, ISO, GMP). Provide concise, accurate, and professional advice.",
          stream: false
        })
      });

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Cannot connect to local Ollama instance. Please ensure Ollama is running.' }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <Activity size={28} className="brand-icon" />
          <h1>GlobalRegAI</h1>
        </div>
        
        <nav className="nav-menu">
          <button className="nav-item active">
            <Send size={20} />
            <span>Chat Assistant</span>
          </button>
          <button className="nav-item">
            <Database size={20} />
            <span>Knowledge Base</span>
          </button>
          <button className="nav-item">
            <Map size={20} />
            <span>Global Regulations</span>
          </button>
          <button className="nav-item">
            <Settings size={20} />
            <span>Settings</span>
          </button>
        </nav>

        <div className="status-indicator">
          <div className="dot online"></div>
          <span>Local Engine: Ready</span>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="chat-area">
        <header className="chat-header">
          <h2>Regulatory Assistant</h2>
          <span className="badge">100% Local & Free</span>
        </header>
        
        <div className="messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="avatar">
                {msg.role === 'assistant' ? 'AI' : 'U'}
              </div>
              <div className="content">{msg.content}</div>
            </div>
          ))}
          {isTyping && (
            <div className="message assistant typing">
              <div className="avatar">AI</div>
              <div className="content">Thinking...</div>
            </div>
          )}
        </div>

        <div className="input-area">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about FDA 510(k), ISO 13485, or EMA guidelines..." 
          />
          <button className="send-btn" onClick={sendMessage}>
            <Send size={20} />
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;
