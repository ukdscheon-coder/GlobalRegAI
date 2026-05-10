import { useState, useEffect } from 'react';
import { Send, Settings, Database, Activity, Map, LogOut } from 'lucide-react';
import Auth from './components/Auth';
import { supabase } from './lib/supabase';

function App() {
  const [messages, setMessages] = useState([{ role: 'system', content: 'Welcome to GlobalRegAI. How can I assist you with regulatory affairs today?' }]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [session, setSession] = useState<any>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  if (!session) {
    return <Auth onLogin={() => {}} />;
  }

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
          <button className="nav-item" onClick={handleLogout} style={{ marginTop: 'auto', color: '#ef4444' }}>
            <LogOut size={20} />
            <span>Sign Out</span>
          </button>
        </nav>

        <div className="status-indicator">
          <div className="dot online"></div>
          <span>Cloud DB: Connected</span>
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
