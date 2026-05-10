# 🤖 GlobalRegAI — Codex 합류 브리핑
# 작성: Claude | 날짜: 2026-05-10
# 목적: Codex가 현재 상황을 즉시 파악하고 협업에 합류하기 위한 문서

---

## 1. 프로젝트 개요

**프로젝트명:** GlobalRegAI  
**소유자:** uk.dscheon@gmail.com  
**목표:** 전 세계 의료기기·의약품·화장품·식품 인허가·GMP·Audit 전문 AI SaaS  
**수익화:** GitHub 공개 오픈소스 → Vercel 무료 배포 → 구독 유료화  
**현재 버전:** v1.1 (Cloud Edition, Groq API 기반)

---

## 2. 현재 실행 중인 시스템

```
docker compose -f docker-compose.cloud.yml up -d  ← 실행 완료 ✅
```

| 컨테이너 | 포트 | 상태 | 역할 |
|----------|------|------|------|
| globalregai-webui | 3000 | ✅ Running | Open WebUI 채팅 인터페이스 |
| globalregai-proxy | 8000 | ✅ Running | FastAPI 다국어 LLM 프록시 |
| globalregai-n8n | 5678 | ✅ Running | 워크플로우 자동화 |
| globalregai-qdrant | 6333 | ✅ Running | 벡터 DB (RAG) |
| globalregai-searxng | 8080 | ✅ Running | 자체 검색엔진 |

**LLM 엔진:** Groq API (Llama-3.3-70b-versatile) — 무료  
**API 키:** .env에 GROQ_API_KEY 설정 완료

---

## 3. 전체 파일 구조

```
C:\Users\laser\GlobalRegAI\
│
├── docker-compose.cloud.yml     ← 현재 실행 중인 클라우드 버전
├── docker-compose.yml           ← 로컬 Ollama 버전 (GPU 필요, 미사용)
├── .env                         ← GROQ_API_KEY 포함 (git 제외)
│
├── scripts/
│   ├── llm_proxy.py             ← FastAPI 프록시 (Antigravity 작성)
│   ├── groq_client.py           ← Groq API 클라이언트 (Antigravity 작성)
│   ├── language_manager.py      ← 5개국어 자동감지 (Antigravity 작성)
│   ├── data_crawler.py          ← 17개 소스 크롤러 (Claude 작성)
│   ├── pdf_bulk_downloader.py   ← 30개 PDF 다운로더 (Claude 작성)
│   ├── regulatory_sources_registry.py ← 전체 소스 등록소 (Claude 작성)
│   ├── auto_scheduler.py        ← 24/7 자동 스케줄러 (Claude 작성)
│   └── ingest_regulatory_docs.py ← 기본 RAG 수집
│
├── config/
│   ├── open-webui/system_prompt.md  ← 5개국어 규정 전문가 AI 페르소나
│   ├── searxng/settings.yml
│   └── languages/
│       ├── language_config.json
│       ├── regulatory_terms_ko.md   ← MFDS 한국어 용어
│       ├── regulatory_terms_en.md   ← FDA/EMA 영어 용어
│       ├── regulatory_terms_zh.md   ← NMPA 중국어 용어
│       ├── regulatory_terms_ja.md   ← PMDA 일본어 용어
│       └── regulatory_terms_es.md   ← AEMPS/COFEPRIS 스페인어 용어
│
├── n8n-workflows/
│   ├── gmp_audit_checklist.json    ← GMP 감사 체크리스트 자동생성
│   ├── regulatory_search.json      ← 매일 FDA 정보 자동수집
│   └── capa_writer.json            ← CAPA 보고서 자동작성
│
├── COLLABORATION_LOG.md         ← AI 협업 로그 (Claude + Antigravity)
├── ANTIGRAVITY_BRIEFING.md      ← Antigravity용 컨텍스트
└── PROJECT_STRUCTURE.md         ← 전체 구조 설명
```

---

## 4. 3개 AI 역할 분담 현황

| AI | 담당 영역 | 완료 | 진행 중 |
|----|-----------|------|---------|
| **Antigravity** | 인프라·엔진·프록시·아키텍처 | groq_client, llm_proxy, language_manager, docker-compose.cloud | Cosmos Command Center |
| **Claude** | 데이터·크롤러·지식베이스·문서 | 크롤러 17종, PDF 30종, 용어집 5개국어, n8n 워크플로우 | GitHub CI/CD, 크롤러 강화 |
| **Codex** | **코드 품질·테스트·GitHub·프론트엔드** | ← **여기가 Codex 담당** | 아래 참조 |

---

## 5. Codex에게 요청하는 작업 (우선순위 순)

### 🔴 Task 1 — llm_proxy.py import 버그 수정 (즉시)

**파일:** `scripts/llm_proxy.py`

**문제:** Docker 컨테이너 내부에서 import 경로 오류 가능성
```python
# 현재 (버그 가능)
from scripts.groq_client import GroqClient
from scripts.language_manager import LanguageManager

# 수정 필요
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from groq_client import GroqClient
from language_manager import LanguageManager
```

---

### 🔴 Task 2 — language_manager.py 절대경로 수정 (즉시)

**파일:** `scripts/language_manager.py` 15번째 줄

```python
# 현재 (Docker 내부에서 실패)
self.base_path = Path("C:/Users/laser/GlobalRegAI")

# 수정 필요
self.base_path = Path(os.getenv("APP_BASE_PATH", 
                      os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
```

---

### 🔴 Task 3 — GitHub 공개 배포 설정

```bash
# 1. .gitignore 확인 (.env 제외 필수)
# 2. GitHub 신규 저장소 생성: GlobalRegAI (Public)
# 3. 첫 커밋 & 푸시
git init
git add .
git commit -m "feat: GlobalRegAI v1.1 - Free Regulatory AI (5 Languages)"
git branch -M main
git remote add origin https://github.com/[username]/GlobalRegAI.git
git push -u origin main
```

---

### 🟡 Task 4 — 프록시 서버 API 테스트 코드 작성

**파일:** `tests/test_proxy.py` (신규 생성)

```python
# 테스트 항목:
# 1. /v1/chat/completions 엔드포인트 응답 확인
# 2. 한국어 질문 → 한국어 응답 + MFDS 용어 확인
# 3. 스페인어 질문 → 스페인어 응답 + AEMPS 용어 확인
# 4. 영어 질문 → FDA 용어 포함 확인
# 5. Groq API 연결 오류 시 fallback 처리
```

---

### 🟡 Task 5 — GitHub Actions CI/CD 파이프라인

**파일:** `.github/workflows/ci.yml` (신규 생성)

```yaml
# 트리거: main 브랜치 push
# 작업:
# 1. Python 문법 검사 (flake8)
# 2. 테스트 실행 (pytest)
# 3. Docker 이미지 빌드 확인
# 4. Vercel 자동 배포 (나중에 추가)
```

---

### 🟢 Task 6 — Vercel 프론트엔드 Next.js 기초 구조

**디렉토리:** `frontend/` (신규 생성)

```
frontend/
├── app/
│   ├── page.tsx          ← 랜딩 페이지
│   ├── chat/page.tsx     ← 규정 AI 채팅
│   ├── audit/page.tsx    ← GMP 감사 체크리스트
│   └── capa/page.tsx     ← CAPA 보고서 생성기
├── components/
│   ├── LanguageSelector.tsx  ← 5개국어 선택
│   ├── ChatWindow.tsx        ← 채팅 UI
│   └── AgencyBadge.tsx       ← 규제기관 배지
└── package.json
```

---

## 6. 현재 미해결 이슈

| 이슈 | 심각도 | 담당 |
|------|--------|------|
| llm_proxy.py import 경로 | 🔴 Critical | **Codex** |
| language_manager 절대경로 | 🔴 Critical | **Codex** |
| GitHub 미배포 | 🟡 High | **Codex** |
| RAG 데이터 미수집 (Qdrant 비어있음) | 🟡 High | Claude |
| n8n 워크플로우 미등록 | 🟡 Medium | Claude |
| 시스템 프롬프트 미적용 | 🟡 Medium | 사용자 1회 설정 필요 |

---

## 7. 데이터 수집 현황

**Qdrant 벡터 DB 현재 상태:** 비어있음 (수집 필요)

수집 예정 소스 (17개):
- 🇺🇸 FDA: openFDA API (리콜, 510k, 의약품, 식품)
- 🇺🇸 eCFR: 21 CFR Part 820/211/117/700
- 🌍 ICH: Q7·Q8·Q9·Q10·Q11·Q12·E6 PDF
- 🌍 WHO: GMP 가이드라인 PDF
- 🇪🇺 EMA: GMP Annex 1·11, MDR
- 🇰🇷 MFDS: 의료기기·의약품·화장품 규정
- 🇯🇵 PMDA: 의료기기·의약품 가이드라인
- 🇪🇸 AEMPS/COFEPRIS/ANMAT: 스페인·중남미 규정
- ⚗️ REACH/RoHS/OSHA: 화학·전기 규정
- 💬 Reddit/RAPS/PubMed: 커뮤니티 Q&A

---

## 8. 별도 시스템 — Cosmos-AI Command Center

**Antigravity 구축 중** (GlobalRegAI와 완전 분리)
- 포트: **8788**
- 역할: 3개 AI 에이전트 통제 대시보드
- 기능: 실시간 에이전트 상태, agents_chat.json 기반 통신

**Codex는 Command Center 개발에 참여하되 GlobalRegAI 코드와 혼용 금지**

---

## 9. 협업 프로토콜

```
작업 완료 시 → COLLABORATION_LOG.md 업데이트
다음 AI에게 인계 시 → 해당 파일에 "다음 작업" 명시
긴급 이슈 → COLLABORATION_LOG.md 상단에 🚨 표시
```

**공용 작업 공간:** `C:\Users\laser\GlobalRegAI\`  
**통신 파일:** `COLLABORATION_LOG.md`, `agents_chat.json` (Antigravity 생성 예정)

---

## 10. 한 줄 요약

> GlobalRegAI는 현재 Docker로 실행 중이며, Codex의 즉각적인 도움이 필요한 곳은 **import 버그 2건 수정**과 **GitHub 공개 배포**입니다. 나머지는 Claude와 Antigravity가 병렬로 진행 중입니다.

---
*이 문서는 Claude가 작성했습니다. 질문은 COLLABORATION_LOG.md에 남겨주세요.*
