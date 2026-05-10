# GlobalRegAI: 종합 아키텍처 및 개발 백서 (Architecture Master Document)

이 문서는 GlobalRegAI의 탄생부터 현재 Phase 3까지의 전 개발 과정, AI 통합 구조, 해결하고자 하는 비즈니스 목표, 그리고 코딩 구조를 총망라한 **공식 백서(Whitepaper)**입니다. 이 문서는 안전한 곳에 다운로드하여 보관하시기 바랍니다.

---

## 1. 전 개발 과정 요약 (Development History)

* **Phase 1: Foundation (기반 구축)**
  * Electron과 React 기반의 100% 로컬 독립형 규제 AI 앱 구축 완료.
  * 사용자 UI 디자인 (다크/라이트 모드, 반응형 채팅창) 및 Ollama 로컬 LLM 연동.
* **Phase 2: SaaS Monetization (수익화 및 웹 배포)**
  * 개인용 데스크톱 앱을 넘어 전 세계 누구나 접속할 수 있는 웹 기반 SaaS로 전환.
  * Supabase를 통한 회원가입/인증 기능 구현 및 `globalregai.info` 공식 도메인 GitHub Pages 배포.
  * Freemium(무료 맛보기 후 결제) 흐름을 위한 모달(Modal) 팝업 UI 도입.
  * 지정된 이메일(`uk.dscheon@gmail.com`, `admin@globalregai.info`)에만 `[ADMIN]` 권한 및 영구 무료 혜택 부여.
* **Phase 3: RAG 파이프라인 및 클라우드 AI 통합**
  * 웹 접속 시 AI가 대답하지 못하는 한계(로컬 Ollama 의존)를 극복하기 위해 클라우드 AI 라우터로 설계 변경.
  * 전 세계 17개국 주요 규제 기관(FDA, PMDA, NMPA, EMA 등)의 법령을 Supabase `pgvector`로 주입(Ingestion)하는 Python 파이프라인 설계.
  * 답변 시 공식 출처(링크 및 조항)를 의무적으로 달아주는 "Citation System(인용 시스템)" 구축.

---

## 2. AI 아키텍처 구조 (System Architecture)

GlobalRegAI는 일반적인 챗봇이 아닌, **의료기기·의약품·화장품·식품 특화 RAG (Retrieval-Augmented Generation)** 시스템입니다.

### 2.1 하이브리드 인프라스트럭처 (Hybrid Infrastructure)
1. **Frontend (React/Vite)**: 사용자의 질문을 받고 UI를 표시합니다. 
2. **LLM Engine**:
   * 로컬 모드: 인터넷 연결 없이 Ollama (llama3.2)를 통해 기밀문서를 분석합니다.
   * 클라우드 모드 (SaaS): 웹 브라우저에서는 Claude 3.5 Sonnet / OpenAI API로 라우팅되어 가장 똑똑한 답변을 제공합니다.
3. **지식 데이터베이스 (Supabase pgvector)**: 
   * 사용자의 폴더(`C:\Users\laser\GlobalRegAI\rag`)에 모아둔 기존 문서와 ChatGPT/Codex로 생성한 데이터, 그리고 17개국 규제 웹사이트의 수만 페이지가 벡터(수학적 좌표)로 변환되어 저장됩니다.

### 2.2 해결하고자 하는 문제 (Problems Solved)
* **비효율적 규제 검색**: 국가별 규제 기관(FDA, PMDA, TFDA, ASEAN 등)의 웹사이트에 흩어진 파편화된 법규를 AI가 한눈에 취합하여 찾아줍니다.
* **언어 장벽 및 법적 용어 번역**: 단순 구글 번역이 아닌, "각 국가의 공식 규제 용어 사전"을 바탕으로 완벽하게 번역된 답변을 제공합니다. (한국어, 영어, 일본어, 중국어 지원)
* **신뢰성 부족 방지**: AI가 지어내는 말(Hallucination)을 막기 위해 답변 하단에 무조건 `[출처: 해당 규제 기관 링크]`를 첨부하여 법적 근거를 명확히 합니다.

---

## 3. 핵심 코딩 구조 (Code Structure)

현재 프로젝트 폴더(`C:\Users\laser\.gemini\antigravity\scratch\GlobalRegAI`)의 뼈대는 다음과 같습니다.

```text
GlobalRegAI/
├── src/
│   ├── components/
│   │   └── Auth.tsx             # Supabase 기반 로그인/회원가입 팝업(Freemium)
│   ├── lib/
│   │   └── supabase.ts          # 클라우드 데이터베이스(Supabase) 연결 세팅
│   ├── App.tsx                  # 핵심 메인 앱 (채팅 UI, 다국어 선택, Admin 로직, RAG 라우터)
│   └── index.css                # 전체 디자인 스타일링 (라이트/다크 모드 변수)
├── supabase/
│   └── migrations/
│       └── 20260510_init_vector_db.sql # 17개국 규제 문서를 담을 pgvector 스키마 설계도
├── scripts/
│   └── ingest_global_agencies.py # FDA, NMPA, PMDA 등 전 세계 기관의 데이터를 스크래핑하는 Python 엔진
├── package.json                 # npm 라이브러리 및 배포(gh-pages) 스크립트
└── GlobalRegAI_Comprehensive_Manual.md # 사용자 및 관리자용 세부 매뉴얼
```

### 3.1 주요 코드 포인트 (Key Code Snippets)
* **Admin 보안 로직 (`src/App.tsx`)**:
  ```javascript
  const ADMIN_EMAILS = ['uk.dscheon@gmail.com', 'admin@globalregai.info'];
  const isAdmin = session?.user?.email && ADMIN_EMAILS.includes(session.user.email);
  ```
  이 코드는 지정된 두 개의 이메일 외에는 절대 Admin 권한을 부여하지 않는 철통 보안 역할을 합니다.

* **17개국 기관 답변 생성 로직 (`src/App.tsx`)**:
  사용자의 질문에서 'FDA', 'PMDA', 'NMPA' 등 국가 키워드를 추출하여 해당 기관의 가장 정확한 가이드라인과 공식 홈페이지 링크를 매칭하여 답변합니다.

---

## 4. 향후 남은 작업 (Next Steps)
* 기존 `C:\Users\laser\GlobalRegAI\n8n-workflows` 에 있는 자동화 시나리오(CAPA 생성 등)를 클라우드 서버리스 API로 포팅.
* Stripe를 연동하여 `Community (Free)` 유저가 월 구독 결제를 할 수 있도록 결제창 구축.

> **이 문서는 GlobalRegAI의 핵심 기밀이자 아키텍처 문서입니다. 안전한 폴더에 이동시켜 보관해 주십시오.**
