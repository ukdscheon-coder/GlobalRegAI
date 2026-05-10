# GlobalRegAI — Antigravity 협업 브리핑 문서
# 작성일: 2026-05-10
# 목적: Antigravity Local AI가 GlobalRegAI를 이해하고 강화하기 위한 완전한 컨텍스트

---

## 1. 프로젝트 개요

**프로젝트명:** GlobalRegAI  
**목적:** 전 세계 의료기기·의약품·화장품·식품 인허가, GMP, Audit 전문 AI SaaS  
**소유자:** uk.dscheon@gmail.com  
**상태:** MVP 로컬 버전 완성, 공개 배포 준비 중  
**라이선스:** 오픈소스 컴포넌트 기반 (MIT/Apache 2.0)  

---

## 2. 현재 파일 구조 (저장 위치: C:\Users\laser\GlobalRegAI\)

```
GlobalRegAI/
├── docker-compose.yml              ← 5개 서비스 정의
├── .env.example                    ← 환경변수 템플릿
├── README.md                       ← 설치 가이드
├── PROJECT_STRUCTURE.md            ← 이 문서와 함께 읽을 구조 설명
│
├── [Windows 스크립트]
│   ├── setup-windows.bat
│   ├── start-windows.bat
│   ├── stop-windows.bat
│   └── load-regulatory-docs.bat
│
├── [Mac 스크립트]
│   ├── setup-mac.sh
│   ├── start-mac.sh
│   ├── stop-mac.sh
│   └── load-regulatory-docs.sh
│
├── config/
│   ├── open-webui/
│   │   └── system_prompt.md        ← AI 페르소나 (5개국어 완전 지원)
│   ├── searxng/
│   │   └── settings.yml
│   └── languages/                  ← [v1.1 신규] 다국어 규정 용어집
│       ├── language_config.json    ← 5개국어 설정
│       ├── regulatory_terms_ko.md  ← MFDS 한국어 용어
│       ├── regulatory_terms_en.md  ← FDA/EMA 영어 용어
│       ├── regulatory_terms_zh.md  ← NMPA 중국어 용어
│       ├── regulatory_terms_ja.md  ← PMDA 일본어 용어
│       └── regulatory_terms_es.md  ← AEMPS/COFEPRIS/ANMAT 스페인어 용어
│
├── scripts/
│   └── ingest_regulatory_docs.py   ← RAG 지식베이스 구축 (FDA/EMA/MFDS/ISO)
│
└── n8n-workflows/
    ├── gmp_audit_checklist.json
    ├── regulatory_search.json
    └── capa_writer.json
```

---

## 3. 기술 스택

### 현재 (로컬 버전)
```
LLM 엔진:     Ollama (llama3.2:3b)
임베딩:       nomic-embed-text
벡터 DB:      Qdrant (포트 6333)
채팅 UI:      Open WebUI (포트 3000)
자동화:       n8n (포트 5678)
검색:         SearXNG (포트 8080)
컨테이너:     Docker Compose
```

### 공개 배포 목표 (Antigravity 작업 필요)
```
LLM 엔진:     Groq API (무료, Llama3-70b) 또는 Cloudflare Workers AI
임베딩:       Groq / HuggingFace Inference API (무료)
벡터 DB:      Supabase pgvector (무료 500MB) 또는 Qdrant Cloud 무료 tier
프론트엔드:   Next.js 14 + Vercel (무료 배포)
백엔드 API:   FastAPI 또는 Next.js API Routes
자동화:       GitHub Actions (무료) 대체 n8n
DB/인증:      Supabase (무료 tier)
결제:         Stripe (나중에 추가)
도메인:       GitHub Pages 또는 Vercel 무료 도메인
```

---

## 4. 핵심 기능 목록

### 현재 구현된 기능
- [x] 5개국어 규정 Q&A (한/영/중/일/스페인어)
- [x] GMP 감사 체크리스트 자동 생성 (n8n webhook)
- [x] CAPA 보고서 자동 작성 (n8n webhook)
- [x] FDA 리콜/시행 정보 매일 자동 수집
- [x] 규정 문서 RAG 지식베이스 (FDA/EMA/MFDS/ISO/AEMPS)
- [x] 자체 웹검색 (SearXNG)
- [x] Windows + macOS 지원

### Antigravity가 추가해야 할 기능 (우선순위 순)

#### 🔴 최우선 (공개 배포를 위해 필수)
1. **Groq API 연동** — Ollama를 Groq 무료 API로 교체
   - 환경변수: `GROQ_API_KEY` (console.groq.com에서 무료 발급)
   - 모델: `llama-3.3-70b-versatile` (무료)
   - Open WebUI에서 Groq API 연결 설정

2. **GitHub 공개 배포**
   - `.env` 제외한 모든 파일 push
   - GitHub Actions workflow 추가
   - README 영문화 (글로벌 사용자용)

3. **언어 자동감지 → 자동 응답**
   - 사용자 입력 언어 자동 감지
   - system_prompt에 언어별 규정 용어 동적 주입

#### 🟡 중요 (사용성 향상)
4. **Vercel 프론트엔드 구축**
   ```
   /                    ← 랜딩 페이지
   /chat                ← 규정 AI 채팅
   /audit-checklist     ← GMP 감사 체크리스트 생성기
   /capa-generator      ← CAPA 보고서 생성기
   /regulatory-updates  ← 최신 규정 업데이트 피드
   ```

5. **Supabase 연동**
   - 사용자 세션 관리
   - 대화 히스토리 저장
   - 규정 문서 벡터 저장

6. **문서 업로드 & 분석 기능**
   - PDF SOP 업로드 → AI 분석
   - 규정 적합성 자동 체크

#### 🟢 장기 과제
7. **MFDS 한국어 규정 데이터 확장**
   - 고시, 가이드라인 자동 크롤링
   - MFDS 공식 API 활용

8. **FDA RSS 피드 실시간 연동**
   - https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds
   - 신규 가이던스 자동 알림

9. **다국어 규정 비교 기능**
   - "이 제품을 FDA와 MFDS 동시 허가하려면?" 형태 질의 지원

10. **모바일 반응형 UI**

---

## 5. API 엔드포인트 (현재 n8n webhooks)

```
POST http://localhost:5678/webhook/gmp-audit
  Body: { "facility_type": "...", "framework": "FDA", "product_category": "..." }
  Returns: GMP 감사 체크리스트 JSON

POST http://localhost:5678/webhook/generate-capa
  Body: { "finding_type": "...", "description": "...", "area": "...", "framework": "...", "classification": "Major" }
  Returns: CAPA 보고서 텍스트

GET http://localhost:6333/collections/globalregai_regulations
  Returns: 규정 벡터 DB 컬렉션 정보
```

---

## 6. 다국어 지원 상세 (v1.1)

### 지원 언어 및 규제기관
| 코드 | 언어 | 주요 규제기관 | 관련 규정 |
|------|------|--------------|-----------|
| `ko` | 한국어 | MFDS (식품의약품안전처) | 의료기기법, 약사법, 화장품법 |
| `en` | English | FDA, EMA, TGA, Health Canada | 21 CFR, EU MDR, ISO |
| `zh` | 中文 | NMPA (国家药品监督管理局) | 医疗器械监督管理条例 |
| `ja` | 日本語 | PMDA, 厚生労働省 | 薬機法, GMP省令 |
| `es` | Español | AEMPS, COFEPRIS, ANMAT, INVIMA | MDR, NOM-059, Disposiciones ANMAT |

### 언어 설정 파일 위치
```
config/languages/language_config.json     ← 전체 언어 설정
config/languages/regulatory_terms_ko.md  ← 한국어 용어
config/languages/regulatory_terms_en.md  ← 영어 용어
config/languages/regulatory_terms_zh.md  ← 중국어 용어
config/languages/regulatory_terms_ja.md  ← 일본어 용어
config/languages/regulatory_terms_es.md  ← 스페인어 용어 (신규 추가)
```

---

## 7. 수익화 로드맵

```
Phase 1 (현재~1개월): GitHub 공개 오픈소스
  → Star 확보, 커뮤니티 구축
  → Reddit r/regulatoryaffairs 홍보
  → LinkedIn 규정 전문가 그룹 홍보

Phase 2 (1~3개월): Vercel 무료 배포 SaaS
  → 무료 플랜으로 사용자 확보
  → GitHub Sponsors 활성화

Phase 3 (3~6개월): 유료 플랜 도입
  → Basic $29/월, Pro $99/월
  → Stripe 결제 연동

Phase 4 (6개월~): 기업 고객
  → 제약/의료기기 회사 B2B
  → 연간 계약 $10,000~
```

---

## 8. Antigravity에게 요청하는 작업

### 즉시 시작 가능한 작업

**Task 1: Groq API 연동 코드 작성**
```python
# scripts/groq_client.py 신규 생성
# Ollama API와 동일한 인터페이스로 Groq 호출
# GROQ_API_KEY 환경변수 사용
# 모델: llama-3.3-70b-versatile
```

**Task 2: 언어 자동감지 미들웨어**
```python
# scripts/language_detector.py 신규 생성
# 입력 텍스트 → 언어 감지 → 해당 언어 규정 용어 로드
# config/languages/ 폴더의 용어집 동적 로드
```

**Task 3: GitHub README 국제화**
```
README.md → 영문 메인
README_ko.md → 한국어
README_es.md → 스페인어
```

**Task 4: Docker Compose → Groq 버전 분리**
```
docker-compose.yml         ← 현재 (로컬 Ollama)
docker-compose.cloud.yml   ← 신규 (Groq API, 공개 배포용)
```

---

## 9. 참고 자료 (벤치마킹 소스)

| 소스 | URL | 용도 |
|------|-----|------|
| FDA Guidance | https://www.fda.gov/regulatory-information | 미국 규정 |
| FDA API | https://api.fda.gov | 리콜/시행 실시간 데이터 |
| EMA Guidelines | https://www.ema.europa.eu/en/documents | EU 규정 |
| MFDS | https://www.mfds.go.kr | 한국 규정 |
| NMPA | https://www.nmpa.gov.cn | 중국 규정 |
| PMDA | https://www.pmda.go.jp | 일본 규정 |
| AEMPS | https://www.aemps.gob.es | 스페인 규정 |
| COFEPRIS | https://www.gob.mx/cofepris | 멕시코 규정 |
| ANMAT | https://www.argentina.gob.ar/anmat | 아르헨티나 규정 |
| RegGuard Paper | https://arxiv.org/html/2601.17826v1 | RAG 설계 참고 |
| local-ai-packaged | https://github.com/coleam00/local-ai-packaged | 아키텍처 참고 |

---

## 10. 연락처
- Email: uk.dscheon@gmail.com
- 개발 도구: Claude Code (Anthropic) + Antigravity Local
- 협업 방식: Claude → 설계/코드 생성 → GitHub → Antigravity → 강화/배포
