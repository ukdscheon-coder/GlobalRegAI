import { useState, useEffect } from 'react';
import { Send, Settings, Database, Activity, Map, LogOut, Globe, Sun, Moon } from 'lucide-react';
import Auth from './components/Auth';
import { supabase } from './lib/supabase';

function App() {
  const [messages, setMessages] = useState([{ role: 'system', content: 'Welcome to GlobalRegAI. How can I assist you with regulatory affairs today? Feel free to ask a question!' }]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [session, setSession] = useState<any>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [theme, setTheme] = useState('light');
  const [language, setLanguage] = useState('English');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      if (session) setShowAuthModal(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  const ADMIN_EMAILS = ['uk.dscheon@gmail.com', 'admin@globalregai.info'];
  const isAdmin = session?.user?.email && ADMIN_EMAILS.includes(session.user.email);

  const sendMessage = async () => {
    if (!input.trim()) return;
    if (!session) {
      setShowAuthModal(true);
      return;
    }
    
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
          <button className="nav-item" onClick={() => !session && setShowAuthModal(true)}>
            <Database size={20} />
            <span>Knowledge Base</span>
          </button>
          <button className="nav-item" onClick={() => !session && setShowAuthModal(true)}>
            <Map size={20} />
            <span>Global Regulations</span>
          </button>
          <button className="nav-item" onClick={() => !session && setShowAuthModal(true)}>
            <Settings size={20} />
            <span>Settings</span>
          </button>
          {session ? (
            <button className="nav-item" onClick={handleLogout} style={{ marginTop: 'auto', color: '#ef4444' }}>
              <LogOut size={20} />
              <span>Sign Out</span>
            </button>
          ) : (
            <button className="nav-item" onClick={() => setShowAuthModal(true)} style={{ marginTop: 'auto', color: '#3b82f6', border: '1px solid #3b82f6' }}>
              <LogOut size={20} style={{transform: 'rotate(180deg)'}} />
              <span>Sign In / Sign Up</span>
            </button>
          )}
        </nav>

        <div className="status-indicator">
          <div className="dot online"></div>
          <span>{session ? 'Cloud DB: Connected' : 'Guest Mode (View Only)'}</span>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="chat-area">
        <header className="chat-header">
          <h2>Regulatory Assistant {isAdmin && <span style={{color: '#f59e0b', fontSize: '0.875rem', marginLeft: '0.5rem'}}>[ADMIN]</span>}</h2>
          <div style={{display: 'flex', gap: '0.75rem', alignItems: 'center'}}>
            {/* Language Selector */}
            <div style={{display: 'flex', alignItems: 'center', gap: '0.25rem', padding: '0.25rem 0.5rem', border: '1px solid var(--border-color)', borderRadius: '0.5rem', backgroundColor: 'var(--bg-color)'}}>
              <Globe size={16} color="var(--text-secondary)" />
              <select value={language} onChange={(e) => setLanguage(e.target.value)} style={{background: 'transparent', border: 'none', color: 'var(--text-primary)', outline: 'none', fontSize: '0.875rem'}}>
                <option>English</option>
                <option>한국어</option>
                <option>日本語</option>
                <option>中文</option>
              </select>
            </div>
            {/* Theme Toggle */}
            <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} style={{background: 'var(--bg-color)', border: '1px solid var(--border-color)', borderRadius: '0.5rem', padding: '0.4rem', cursor: 'pointer', display: 'flex'}}>
              {theme === 'light' ? <Moon size={16} color="var(--text-secondary)" /> : <Sun size={16} color="var(--text-secondary)" />}
            </button>
            {isAdmin ? (
              <span className="badge" style={{backgroundColor: 'rgba(245, 158, 11, 0.1)', color: '#fbbf24', border: '1px solid rgba(245, 158, 11, 0.2)'}}>Free Access (Admin)</span>
            ) : (
              <span className="badge" style={{backgroundColor: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6', border: '1px solid rgba(59, 130, 246, 0.2)'}}>Community (Free)</span>
            )}
          </div>
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
            placeholder={session ? "Ask about FDA 510(k), ISO 13485, or EMA guidelines..." : "Sign in to start asking questions..."}
          />
          <button className="send-btn" onClick={sendMessage}>
            <Send size={20} />
          </button>
        </div>
      </main>

      {/* Auth Modal Overlay */}
      {showAuthModal && (
        <div className="modal-overlay">
          <div className="modal-close-bg" onClick={() => setShowAuthModal(false)}></div>
          <div className="modal-content">
            <button className="modal-close-btn" onClick={() => setShowAuthModal(false)}>✕</button>
            <Auth onLogin={() => setShowAuthModal(false)} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
