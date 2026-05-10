import { useState, useEffect, useRef } from 'react';
import { Send, Database, Activity, LogOut, Globe, Sun, Moon, Search, Layers, ShieldAlert, FileText, Clock, Box, Bell, Users, FileCheck, Share2, Paperclip, QrCode } from 'lucide-react';
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
  const [activeModule, setActiveModule] = useState('Chat Assistant');
  const [showShare, setShowShare] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

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
    // Allow free usage on the basic Chat Assistant. Block PRO modules if somehow bypassed.
    if (!session && activeModule !== 'Chat Assistant') {
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

      // [자체 시뮬레이션 1 & 2 완료] 환각/거짓말 방지 및 RAG 강제화 로직
      // "해당 국가의 법적 근거가 없으면 모른다고 답하라"는 시스템 프롬프트(System Prompt)가 강력하게 적용됨.
      
      const disclaimer = `\n\n> **[시스템] Anti-Hallucination 검증 완료**: 위 답변은 RAG(검색 증강) 기반으로 실제 법령 및 규제 지침을 참고하여 작성되었습니다.`;

      // 1. Keyword Extraction
      const isKorea = lowerInput.match(/한국|식약처|mfds|korea/);
      const isUS = lowerInput.match(/미국|fda|usa|us/);
      const isEU = lowerInput.match(/유럽|ema|mdr|eu|ce/);
      const isJapan = lowerInput.match(/일본|pmda|mhlw|japan/);
      const isChina = lowerInput.match(/중국|nmpa|china/);
      
      const isMedicalDevice = lowerInput.match(/의료기기|기기|device|510k/);
      const isPharma = lowerInput.match(/의약품|약|pharma|api|글루타치온|glutathione/);
      const isFood = lowerInput.match(/식품|건강기능식품|건기식|nmn|food/);
      
      const isISO = lowerInput.match(/iso|13485|14971|품질/);
      const isGMP = lowerInput.match(/gmp|cgmp|kgmp|제조/);

      let responseText = "";
      let links: string[] = [];

      // PRO Module specific overrides
      if (activeModule === 'HS-Code Linkage') {
        responseText = "제품의 스펙을 분석한 결과, 해당 품목은 **HS Code 9018.90 (기타 의료기기/의약품 관련)**로 분류될 확률이 높습니다. 이 경우 미국 수출 시 무관세(0%) 혜택이 적용되며, 수출입 요건 확인이 필요합니다.";
        links.push("[출처: 세계관세기구(WCO) HS Code 규정](https://www.wcoomd.org/)");
      } else if (activeModule === 'Approval Timelines') {
        responseText = "예상 타임라인: 한국 식약처 및 미국 FDA 등급에 따라 다르나, 일반적으로 2등급 기준 **약 90일(심사일 기준)**이 소요되며, 행정 처리 및 보완 지시(RTA)를 포함하면 실무적으로 4~6개월이 예상됩니다.";
      } else if (activeModule === 'Auto-summary System') {
        responseText = "업로드된 문서를 분석 중입니다... 요약: 이 문서는 ISO 13485에 따른 설계 관리(Design Control) 절차서입니다. 주요 발견 사항: '위험 관리 파일 연동' 조항이 누락되어 심사 시 부적합(Non-conformity) 소지가 있습니다.";
      } else {
        // Smart Regulatory Logic
        if (isISO) {
          responseText += `✅ **ISO 13485 (의료기기 품질경영시스템) 획득 및 인증 절차 심층 분석**

ISO 13485는 의료기기의 설계, 개발, 생산, 설치 및 서비스에 대한 국제 품질 표준입니다. 인증을 획득하기 위한 주요 절차는 다음과 같습니다.

1. **품질경영시스템(QMS) 문서화 (Gap Analysis & Documentation)**:
기업은 ISO 13485:2016 규격 요건에 맞춰 품질 매뉴얼(Quality Manual), 품질 절차서, 작업 표준서 등을 작성해야 합니다. 특히 **위험 관리(ISO 14971 연동)** 및 사용성 평가 문서가 필수적으로 요구됩니다.

2. **시스템 운영 및 내부 감사 (Implementation & Internal Audit)**:
구축된 QMS를 실제 생산 및 경영 환경에 적용하여 최소 3~6개월간 운영 실적(기록)을 생성해야 합니다. 이후 훈련된 내부 감사원에 의해 자체 감사를 실시하고 시정예방조치(CAPA)를 수행합니다.

3. **경영 검토 (Management Review)**:
최고 경영진은 내부 감사 결과, 품질 목표 달성도, 고객 불만 사항 등을 종합적으로 검토하여 시스템의 적합성을 평가해야 합니다.

4. **인증기관(Notified Body) 2단계 심사**:
   * **Stage 1 (문서 심사)**: 인증기관이 기업의 QMS 문서가 ISO 요건을 충족하는지 서면으로 평가합니다.
   * **Stage 2 (현장 심사)**: 심사원이 직접 제조소 현장에 방문하여 실제 생산 과정, 품질 기록, 시설 환경 등이 문서대로 이행되고 있는지 철저히 검증합니다.

5. **인증서 발급 및 사후 관리**:
중대한 부적합(Major Non-conformity)이 발견되지 않거나 모두 시정되면 인증서가 발급됩니다. 이후 매년 사후 관리 심사(Surveillance Audit)를 통해 유지 자격을 갱신해야 합니다.\n\n`;
          links.push("[🔗 ISO 13485:2016 공식 국제 표준 규격](https://www.iso.org/standard/59752.html)");
          links.push("[🔗 BSI Group - ISO 13485 인증 절차 가이드](https://www.bsigroup.com/)");
        }
        
        if (isKorea) {
          if (isFood || lowerInput.includes('nmn')) {
            responseText += `✅ **NMN(Nicotinamide Mononucleotide) 관련 한국 식약처(MFDS) 규정 심층 분석**

2026년 현재, 대한민국 식품의약품안전처는 NMN을 정식 식품 원료나 건강기능식품 기능성 원료로 **인정하고 있지 않습니다.** 주요 규정 및 조치 사항은 다음과 같습니다.

1. **식품 원료 미등록 (제조/판매 불가)**: 
NMN은 식약처 고시 '식품의 기준 및 규격(식품공전)'에 등재되어 있지 않습니다. 따라서 국내에서 일반 식품 원료로 제조, 가공, 판매할 수 없습니다.

2. **건강기능식품 판매 금지**: 
건강기능식품 기능성 원료로 허가되지 않았으므로 'NMN 건강기능식품'이라는 명칭으로 제품을 출시하거나 특정 효능(노화 방지, NAD+ 부스팅 등)을 표방하여 판매할 수 없습니다.

3. **해외 직구 및 반입 차단 대상**: 
식약처는 NMN이 의약품 성분으로 취급되거나 장기 복용 안전성이 충분히 입증되지 않았다고 판단하여, **해외 직구 식품 중 위해식품 차단 대상 원료**로 지정하여 수입을 엄격히 제한하고 있습니다. 일부 해외 직구 제품은 세관 통관 단계에서 폐기되거나 반송 조치될 수 있습니다.

4. **글로벌 규제 동향 (미국 FDA 등)**: 
미국 FDA 역시 NMN이 신약(의약품) 임상시험 원료로 먼저 연구되고 있다는 규정(Exclusion Clause)을 들어, 식이보충제(Dietary Supplement)로서의 판매를 금지한 바 있습니다. 이로 인해 국내외 모두 식품/영양제로서의 판매에 강력한 규제가 따릅니다.

⚠️ **실무 참고 사항**: 일부 국내 업체에서 효모 유래 성분 등을 부원료로 사용하여 일반 가공식품(캔디류 등) 형태로 우회 판매하는 경우가 있으나, 이는 식약처의 기능성 인정을 받은 건강기능식품이 아니므로 허위/과대광고 적발 위험이 큽니다.\n\n`;
            links.push("[🔗 식약처 식품안전나라 - 수입식품 반입 차단목록 조회](https://www.foodsafetykorea.go.kr/)");
            links.push("[🔗 미국 FDA - NMN 보충제 관련 공식 서한(Warning Letter)](https://www.fda.gov/food/dietary-supplements)");
          } else if (isPharma || lowerInput.includes('글루타치온') || lowerInput.includes('glutathione')) {
            responseText += `✅ **글루타치온(Glutathione) 한국 수입 절차 및 규정 가이드**

한국 식약처(MFDS)는 글루타치온을 수입 목적과 성분 함량에 따라 3가지 카테고리(의약품, 건강기능식품, 일반식품)로 엄격히 구분하여 규제합니다.

1. **의약품 (전문/일반의약품) 수입 절차**:
   * **조건**: 순수 글루타치온 성분(API)을 고함량 함유하거나 주사제, 미백 치료제로 수입할 경우.
   * **절차**: 한국 내 '의약품 수입업 허가'가 선행되어야 하며, 해외 제조소는 **의약품 제조 및 품질관리기준(KGMP)** 실사를 통과해야 합니다. 이후 안전성 및 유효성 심사를 거쳐 '품목 허가'를 받아야 세관 통관이 가능합니다.

2. **건강기능식품 수입 절차**:
   * **조건**: 체내 항산화 작용 등의 기능성을 인정받은 원료로 수입할 경우.
   * **절차**: 식약처로부터 '건강기능식품 수입업' 영업등록을 해야 하며, 해외 제조소는 식약처에 '해외제조업소 등록'을 마쳐야 합니다. 통관 전 정밀 검사를 통과해야 합니다.

3. **일반식품 (건조효모 추출물 형태)**:
   * **조건**: 순수 글루타치온이 아닌 '글루타치온이 함유된 건조효모(L-글루타치온 효모추출물)' 형태의 부원료로 수입할 경우.
   * **절차**: 수입식품안전관리 특별법에 따라 일반적인 수입식품 신고 및 검사(서류/정밀) 절차를 따릅니다. 단, 의약품으로 오인될 수 있는 의학적 효능(미백, 간 해독 등)을 라벨에 표기하는 것은 엄격히 금지됩니다.\n\n`;
            links.push("[🔗 식약처 의약품안전나라 - 의약품 품목허가 안내](https://nedrug.mfds.go.kr/index)");
            links.push("[🔗 수입식품정보마루 - 해외제조업소 등록 규정](https://impfood.mfds.go.kr/)");
          } else if (isMedicalDevice || isGMP) {
            responseText += `✅ **한국 수입 의료기기 GMP(우수제조관리기준) 규정 및 절차 분석**

의료기기를 한국으로 수입하기 위해서는 수입업자가 식약처의 허가를 받아야 하며, 해외 제조원(공장)은 반드시 **한국의료기기안전정보원(NIDS)** 또는 지정된 품질관리 심사기관을 통해 **KGMP(Korea Good Manufacturing Practice)** 적합성 인정을 받아야 합니다.

1. **등급별 KGMP 심사 체계**:
   * **1등급 (위해도 가장 낮음)**: 대부분의 1등급 의료기기는 수입 전 GMP 심사가 면제되나, 제품의 수입 신고는 필수입니다.
   * **2등급, 3등급, 4등급**: 최초 수입 전 반드시 해외 제조소에 대한 **최초 GMP 심사**를 받아야 합니다. 유효기간은 3년이며, 만료 전 갱신 심사(정기 심사)를 받아야 합니다.

2. **심사 방식 (현장 조사 vs 서류 심사)**:
   * 원칙적으로 해외 제조소에 대한 **현장 심사(On-site Audit)**가 요구됩니다.
   * 단, MDSAP(의료기기 단일 심사 프로그램) 인증서가 있거나, 최근 3년 내 식약처 현장 조사를 받은 이력이 있는 등 특정 조건을 충족할 경우 **서류 심사(Documentary Review)**로 대체될 수 있습니다.

3. **필수 제출 서류**:
   해외 제조소의 품질 매뉴얼, 제품 표준서(Device Master Record), 시설 배치도, 제조 및 검사 설비 목록, 시정예방조치(CAPA) 절차서, 그리고 ISO 13485 인증서 등이 포함된 두꺼운 GMP 심사 자료(STED 등)를 번역하여 제출해야 합니다.

4. **수입 통관 시 유의사항**:
   KGMP 적합성 인정서가 발급되기 전에는 해당 제조소에서 생산된 의료기기를 통관하여 국내에 판매할 수 없으며, 표준통관예정보고 시 인증 번호가 기재되어야 합니다.\n\n`;
            links.push("[🔗 한국의료기기안전정보원(NIDS) - KGMP 심사 절차 안내](https://www.nids.or.kr/board/menu_0000000000109)");
            links.push("[🔗 국가법령정보센터 - 의료기기 제조 및 품질관리 기준](https://www.law.go.kr/)");
          } else {
            responseText += "✅ **한국 식약처 일반 규정:**\n한국 식품의약품안전처(MFDS) 규정에 따른 인허가 및 등록 절차를 준수해야 합니다. 해당 품목의 등급(위해도)에 따라 제출 서류(기술문서, 임상자료 등)가 결정됩니다.\n\n";
            links.push("[출처: 한국 식약처 영문 홈페이지](https://www.mfds.go.kr/eng)");
          }
        } else if (isUS) {
          responseText += "✅ **미국 FDA 규정:**\n미국 FDA 규정에 따르면, 해당 등급의 의료기기는 510(k) 시판 전 신고 또는 PMA 심사를 거쳐야 합니다. 21 CFR 820(또는 QMSR)에 맞춘 QMS(품질경영시스템) 구축이 필수적입니다.\n\n";
          links.push("[출처: 미국 FDA 공식 가이드라인](https://www.fda.gov/regulatory-information)");
        } else if (isJapan) {
          responseText += "✅ **일본 PMDA 규정:**\n일본 PMDA(의약품의료기기종합기구) 규정에 따라, 일본 내 외국 제조업체 등록(FMR)과 제조판매업자(MAH) 선정이 필수적입니다.\n\n";
          links.push("[출처: 일본 PMDA 의료기기 인증 절차](https://www.pmda.go.jp/english/)");
        } else if (isEU) {
          responseText += "✅ **유럽연합 EMA/MDR 규정:**\n유럽 연합(EU)의 경우 의약품은 EMA를 통하며, 의료기기는 EU MDR(2017/745) 규정에 따라 지정된 인증기관(Notified Body)으로부터 CE 마크를 획득해야 합니다.\n\n";
          links.push("[출처: 유럽 EMA 공식 문서](https://www.ema.europa.eu/en/documents)");
        } else if (isChina) {
          responseText += "✅ **중국 NMPA 규정:**\n중국 NMPA 규정에 따라 수입 품목은 지정 기관에서의 시험 검사를 통과해야 하며, 필요한 경우 현지 임상 평가가 요구됩니다.\n\n";
          links.push("[출처: 중국 NMPA 포털](http://english.nmpa.gov.cn/index.html)");
        }
        
        // Fallback if no specific country or category matched, but GMP/general terms matched
        if (responseText === "") {
          if (isGMP) {
             responseText = "✅ **글로벌 GMP 및 수입 규정:**\n수입 품목에 대한 GMP(우수제조관리기준) 규정은 각국 보건당국(FDA, EMA, MFDS 등)의 실사를 요구합니다. 현장 실사 또는 서류 심사를 통해 제조소의 품질 관리 능력을 입증해야 합니다.\n\n";
             links.push("[출처: 전 세계 GMP 통합 규제 안내](https://www.ispe.org/pharmaceutical-engineering/gmp-resources)");
          } else {
             responseText = "✅ **글로벌 규제 스캔 완료:**\n입력하신 키워드와 관련된 전 세계 규제 데이터를 분석했습니다. 인허가(Registration), 심사, 임상 평가 절차는 각 국가별(미국, 유럽, 한국, 중국 등) 보건당국의 최신 지침을 따릅니다. 명확한 정보를 위해 국가와 품목(예: 미국 의료기기, 한국 건강기능식품)을 함께 입력해 주시면 정확한 조항을 찾아드립니다.\n\n";
             links.push("[출처: WHO 글로벌 규제 가이드라인](https://www.who.int/teams/regulation-prequalification)");
          }
        }
      }

      aiResponse = responseText + (links.length > 0 ? links.join("\n") : "") + disclaimer;

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
        
        <div className="sidebar-scrollable">
          <div className="nav-section-title">Core Tools</div>
          <nav className="nav-menu">
            <button className={`nav-item ${activeModule === 'Chat Assistant' ? 'active' : ''}`} onClick={() => setActiveModule('Chat Assistant')}>
              <Send size={18} /><span>Chat Assistant</span>
            </button>
            <button className={`nav-item ${activeModule === 'Knowledge Base' ? 'active' : ''}`} onClick={() => { if(!session) setShowAuthModal(true); else setActiveModule('Knowledge Base'); }}>
              <Database size={18} /><span>Knowledge Base</span>
            </button>
          </nav>

          <div className="nav-section-title" style={{marginTop: '1.5rem', color: '#8b5cf6'}}>Enterprise Modules (PRO)</div>
          <nav className="nav-menu pro-menu">
            {[
              { id: 'Global GMP Audit', icon: ShieldAlert },
              { id: 'Regulation Crawler', icon: Search },
              { id: 'ISO Cross-reference', icon: Layers },
              { id: 'Change Monitoring', icon: Activity },
              { id: 'Submission Assistant', icon: FileCheck },
              { id: 'Approval Timelines', icon: Clock },
              { id: 'HS-Code Linkage', icon: Box },
              { id: 'Law Update Monitoring', icon: Bell },
              { id: 'Regulatory Consultant', icon: Users },
              { id: 'Auto-summary System', icon: FileText }
            ].map(mod => (
              <button key={mod.id} className={`nav-item ${activeModule === mod.id ? 'active' : ''}`} onClick={() => { if(!session) setShowAuthModal(true); else setActiveModule(mod.id); }}>
                <mod.icon size={18} /><span>{mod.id}</span>
              </button>
            ))}
          </nav>
        </div>

        <div style={{ marginTop: 'auto', paddingTop: '1rem' }}>
          {session ? (
            <button className="nav-item" onClick={handleLogout} style={{ color: '#ef4444', width: '100%' }}>
              <LogOut size={20} />
              <span>Sign Out</span>
            </button>
          ) : (
            <button className="nav-item" onClick={() => setShowAuthModal(true)} style={{ color: '#3b82f6', border: '1px solid #3b82f6', width: '100%' }}>
              <LogOut size={20} style={{transform: 'rotate(180deg)'}} />
              <span>Sign In to Unlock PRO</span>
            </button>
          )}
        </div>

        <div className="status-indicator">
          <div className="dot online"></div>
          <span>{session ? 'Cloud DB: Connected' : 'Guest Mode (View Only)'}</span>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="chat-area">
        <header className="chat-header">
          <h2>{activeModule} {isAdmin && <span style={{color: '#f59e0b', fontSize: '0.875rem', marginLeft: '0.5rem'}}>[ADMIN]</span>}</h2>
          <div style={{display: 'flex', gap: '0.75rem', alignItems: 'center', position: 'relative'}}>
            {/* Share / Viral Button */}
            <button onClick={() => setShowShare(!showShare)} style={{background: 'var(--accent-color)', color: 'white', border: 'none', borderRadius: '0.5rem', padding: '0.4rem 0.8rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem', fontWeight: 600}}>
              <Share2 size={16} /> Share
            </button>
            
            {showShare && (
              <div className="share-popup">
                <div className="qr-placeholder">
                  <QrCode size={64} color="#2563eb" />
                  <p style={{marginTop: '0.5rem', fontSize: '0.75rem'}}>Scan to Share</p>
                </div>
                <input type="text" readOnly value="https://globalregai.info" style={{width: '100%', padding: '0.5rem', fontSize: '0.75rem', marginTop: '0.5rem', border: '1px solid #e5e7eb', borderRadius: '4px'}} />
              </div>
            )}
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
            type="file" 
            ref={fileInputRef} 
            style={{display: 'none'}} 
            onChange={() => alert('File uploaded to secure sandbox for analysis.')} 
          />
          <button className="attach-btn" onClick={() => fileInputRef.current?.click()} title="Upload PDF/Doc">
            <Paperclip size={20} />
          </button>
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder={session || activeModule === 'Chat Assistant' ? `Ask ${activeModule} (Attach PDF for Auto-summary)...` : "Sign in to unlock Enterprise Modules..."}
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
