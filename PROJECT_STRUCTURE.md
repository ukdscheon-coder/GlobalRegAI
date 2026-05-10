# GlobalRegAI — 전체 프로젝트 구조 (Antigravity 공유용)

## 저장 위치
```
C:\Users\laser\GlobalRegAI\
```

## 디렉토리 트리
```
GlobalRegAI/
│
├── docker-compose.yml              ← 전체 서비스 정의 (핵심)
├── .env.example                    ← 환경변수 템플릿
├── .env                            ← 실제 환경변수 (gitignore)
├── .gitignore
├── README.md                       ← 설치/사용 가이드 (EN+KR)
│
├── setup-windows.bat               ← Windows 최초 설치 스크립트
├── start-windows.bat               ← Windows 시작
├── stop-windows.bat                ← Windows 종료
├── setup-mac.sh                    ← macOS 최초 설치 스크립트
├── start-mac.sh                    ← macOS 시작
├── stop-mac.sh                     ← macOS 종료
│
├── load-regulatory-docs.bat        ← 규정 지식베이스 로드 (Windows)
├── load-regulatory-docs.sh         ← 규정 지식베이스 로드 (Mac)
│
├── config/
│   ├── open-webui/
│   │   └── system_prompt.md        ← AI 페르소나 정의 (5개국어)
│   └── searxng/
│       └── settings.yml            ← 검색엔진 설정
│
├── scripts/
│   └── ingest_regulatory_docs.py   ← FDA/EMA/MFDS/ISO/AEMPS RAG 수집
│
├── n8n-workflows/
│   ├── gmp_audit_checklist.json    ← GMP 감사 체크리스트 자동생성
│   ├── regulatory_search.json      ← 매일 FDA 최신정보 자동수집
│   └── capa_writer.json            ← CAPA 보고서 자동작성
│
├── config/languages/               ← [신규] 다국어 설정
│   ├── language_config.json        ← 5개국어 설정
│   ├── regulatory_terms_ko.md      ← 한국어 규정 전문용어
│   ├── regulatory_terms_en.md      ← 영어 규정 전문용어
│   ├── regulatory_terms_zh.md      ← 중국어 규정 전문용어
│   ├── regulatory_terms_ja.md      ← 일본어 규정 전문용어
│   └── regulatory_terms_es.md      ← 스페인어 규정 전문용어 [신규]
│
├── rag/
│   └── regulatory-docs/            ← 규정 문서 저장 폴더
│
└── assets/                         ← 이미지/로고 등
```

## 서비스 구조 (Docker)
```
┌─────────────────────────────────────────────────────────────┐
│                    GlobalRegAI Stack                         │
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────┐  │
│  │   Ollama    │   │ Open WebUI  │   │      n8n        │  │
│  │  (LLM 엔진) │◄──│  (채팅 UI)  │   │  (자동화 엔진)   │  │
│  │  :11434     │   │   :3000     │   │    :5678        │  │
│  └─────────────┘   └─────────────┘   └─────────────────┘  │
│        ▲                                      │             │
│        │           ┌─────────────┐            ▼             │
│   임베딩/RAG        │   Qdrant    │   ┌─────────────────┐  │
│        └───────────│ (벡터 DB)   │   │   SearXNG       │  │
│                    │   :6333     │   │  (자체검색엔진)   │  │
│                    └─────────────┘   │    :8080        │  │
│                                      └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 포트 맵
| 서비스 | 포트 | 역할 |
|--------|------|------|
| Open WebUI | 3000 | 메인 채팅 인터페이스 |
| n8n | 5678 | 워크플로우 자동화 |
| SearXNG | 8080 | 자체 웹검색 |
| Ollama | 11434 | LLM 모델 서버 |
| Qdrant | 6333 | 벡터 DB (RAG) |
| Qdrant gRPC | 6334 | 벡터 DB (gRPC) |

## 현재 지원 언어 (v1.1)
| 코드 | 언어 | 담당 규제기관 |
|------|------|--------------|
| ko | 한국어 | MFDS (식품의약품안전처) |
| en | English | FDA (US), EMA (EU) |
| zh | 中文 | NMPA (国家药品监督管理局) |
| ja | 日本語 | PMDA (医薬品医療機器総合機構) |
| es | Español | AEMPS (스페인), COFEPRIS (멕시코), ANMAT (아르헨티나) |

## 기술 스택
- **LLM**: Ollama (로컬) → Groq API (배포용, 무료)
- **임베딩**: nomic-embed-text
- **벡터DB**: Qdrant
- **프론트엔드**: Open WebUI (MIT 라이선스)
- **자동화**: n8n
- **검색**: SearXNG

## 다음 개발 우선순위 (Antigravity 작업 목록)
1. Groq API 연동 (공개 배포용 무료 LLM)
2. Vercel 프론트엔드 (Next.js)
3. 사용자 언어 선택 UI (5개국어)
4. AEMPS/COFEPRIS 규정 데이터 추가 (스페인어)
5. FDA RSS 피드 실시간 크롤링
6. GitHub Actions CI/CD 파이프라인
