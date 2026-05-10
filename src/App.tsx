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
      // Simulate Cloud API / Supabase Edge Function Latency
      await new Promise(r => setTimeout(r, 1500));
      
      let aiResponse = "";
      const lowerInput = input.toLowerCase();

      // Simulated RAG Logic handling the 17 global agencies
      if (lowerInput.includes('fda') || lowerInput.includes('미국')) {
        aiResponse = "미국 FDA(식품의약국) 규정에 따르면, 해당 등급의 의료기기는 **510(k)** 시판 전 신고 또는 **PMA** 심사를 거쳐야 합니다. 최신 21 CFR 820 규정에 맞춘 QMS(품질경영시스템) 구축이 필수적입니다.\n\n[출처: 미국 FDA 공식 가이드라인](https://www.fda.gov/regulatory-information)";
      } else if (lowerInput.includes('pmda') || lowerInput.includes('일본')) {
        aiResponse = "일본 PMDA(의약품의료기기종합기구) 및 후생노동성(MHLW)의 규정에 따라, 일본 내 외국 제조업체 등록(FMR)과 제조판매업자(MAH) 선정이 필요합니다.\n\n[출처: 일본 PMDA 의료기기 인증 절차](https://www.pmda.go.jp/english/)";
      } else if (lowerInput.includes('nmpa') || lowerInput.includes('중국')) {
        aiResponse = "중국 NMPA(국가의약품감독관리국) 규정에 따라 모든 수입 의료기기는 현지 임상 평가 또는 해외 임상 데이터 승인을 받아야 하며, NMPA 지정 기관에서 시험 검사를 통과해야 합니다.\n\n[출처: 중국 NMPA 영문 포털](http://english.nmpa.gov.cn/index.html)";
      } else if (lowerInput.includes('유럽') || lowerInput.includes('ema') || lowerInput.includes('mdr')) {
        aiResponse = "유럽 연합(EU)의 경우, 의약품은 EMA(유럽의약품청)를 통하며, 의료기기는 EU MDR(2017/745) 규정에 따라 지정된 인증기관(Notified Body, NB)으로부터 CE 마크를 획득해야 합니다.\n\n[출처: 유럽 EMA 공식 문서](https://www.ema.europa.eu/en/documents)";
      } else if (lowerInput.includes('한국') || lowerInput.includes('식약처') || lowerInput.includes('mfds')) {
        aiResponse = "한국 식품의약품안전처(MFDS)의 규정에 따라, 의료기기는 위해도에 따라 1~4등급으로 분류되며, 2등급 이상의 경우 기술문서 심사 및 한국의료기기안전정보원(NIDS)의 승인이 필요합니다.\n\n[출처: 한국 식약처 영문 홈페이지](https://www.mfds.go.kr/eng)";
      } else {
        aiResponse = "질문하신 내용에 대한 각국의 규제(GMP, ISO, 등급 분류 등)를 스캔 중입니다. 정확한 문맥을 위해 대상 국가(예: 미국, 중국, 일본, 유럽 등)나 품목(의료기기, 의약품, 화장품, 식품)을 조금 더 구체적으로 명시해 주시면 17개 글로벌 규제 기관 데이터베이스에서 해당 법령 및 조항 링크를 찾아 제공해 드리겠습니다.";
      }

      setMessages(prev => [...prev, { role: 'assistant', content: aiResponse }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: '서버 연결 오류: 클라우드 AI 서버에 접속할 수 없습니다.' }]);
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
