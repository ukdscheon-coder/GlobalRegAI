# GlobalRegAI 🌍

> **Free, Open-Source AI for Global Regulatory Affairs**  
> Medical Devices · Pharmaceuticals · Cosmetics · Food · GMP · Audits

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama3.3--70B-orange)](https://groq.com)
[![Languages](https://img.shields.io/badge/Languages-5%20(KO%2FEN%2FZH%2FJA%2FES)-green)](#)

---

## What is GlobalRegAI?

GlobalRegAI is a **100% free, self-hosted AI assistant** for regulatory professionals worldwide.  
It answers questions about regulations from FDA, EMA, MFDS, PMDA, NMPA, AEMPS, COFEPRIS, and more — in **5 languages**, automatically.

| Language | Agencies |
|----------|---------|
| 🇰🇷 Korean | MFDS (식품의약품안전처) |
| 🇺🇸 English | FDA, EMA, TGA, Health Canada |
| 🇨🇳 Chinese | NMPA (国家药品监督管理局) |
| 🇯🇵 Japanese | PMDA (医薬品医療機器総合機構) |
| 🇪🇸 Spanish | AEMPS, COFEPRIS, ANMAT, INVIMA |

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│  Open WebUI (localhost:3000)  ─── Chat Interface │
└───────────────┬─────────────────────────────────┘
                │ OpenAI-compatible API
┌───────────────▼─────────────────────────────────┐
│  LLM Proxy (localhost:8000)  ─── FastAPI         │
│  · Language auto-detection (KO/EN/ZH/JA/ES)      │
│  · Regulatory terminology injection              │
└───────────────┬─────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────┐
│  Groq API  ─── Llama-3.3-70B-Versatile (FREE)   │
└─────────────────────────────────────────────────┘
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────────┐
│ Qdrant:6333  │ │ SearXNG:8080│ │ n8n:5678       │
│ Vector DB    │ │ Web Search  │ │ Automation     │
│ (RAG)        │ │ (Self-hosted│ │ Workflows      │
└──────────────┘ └─────────────┘ └────────────────┘
```

---

## Quick Start (5 minutes)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac/Linux)
- [Free Groq API Key](https://console.groq.com/keys) (takes 1 minute)

### 1. Clone & Configure
```bash
git clone https://github.com/YOUR_USERNAME/GlobalRegAI.git
cd GlobalRegAI

# Copy and edit environment file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 2. Start All Services
```bash
docker compose -f docker-compose.cloud.yml up -d
```

### 3. Open the Chat Interface
Visit **http://localhost:3000** in your browser.

That's it! Ask questions in Korean, English, Chinese, Japanese, or Spanish. 🎉

---

## Services

| Service | Port | Description |
|---------|------|-------------|
| Open WebUI | 3000 | Chat interface (ChatGPT-like) |
| LLM Proxy | 8000 | Multilingual FastAPI middleware |
| n8n | 5678 | Workflow automation |
| Qdrant | 6333 | Vector DB for RAG |
| SearXNG | 8080 | Self-hosted web search |

---

## Data Sources (17 Agencies)

- 🇺🇸 **FDA**: openFDA API, eCFR (21 CFR Part 820/211/117/700)
- 🌍 **ICH**: Q7, Q8, Q9, Q10, Q11, Q12, E6 guidelines
- 🌍 **WHO**: GMP guidelines
- 🇪🇺 **EMA**: GMP Annex 1 & 11, MDR 2017/745
- 🇰🇷 **MFDS**: Medical device, pharmaceutical, cosmetic regulations
- 🇯🇵 **PMDA**: Medical device and pharmaceutical guidelines
- 🇨🇳 **NMPA**: Medical device and pharmaceutical regulations
- 🇪🇸 **AEMPS / COFEPRIS / ANMAT**: Spain & Latin America
- ⚗️ **REACH / RoHS / OSHA**: Chemical and electrical safety
- 💬 **Reddit / RAPS / PubMed**: Community Q&A

---

## Example Questions

```
🇰🇷 "MFDS 의료기기 3등급 인허가 절차를 설명해주세요"
🇺🇸 "What are the FDA 21 CFR Part 820 QMS requirements?"
🇪🇸 "¿Cómo registro un dispositivo médico en COFEPRIS México?"
🇯🇵 "PMDAへの医療機器申請の流れを教えてください"
🇨🇳 "NMPA医疗器械注册流程是什么？"
```

---

## Free Forever

| Component | Cost | Provider |
|-----------|------|---------|
| LLM (Llama 3.3 70B) | **FREE** | Groq |
| Hosting | **FREE** | Self-hosted Docker |
| Vector DB | **FREE** | Qdrant (self-hosted) |
| Web Search | **FREE** | SearXNG (self-hosted) |
| Automation | **FREE** | n8n (self-hosted) |

---

## License

MIT License — free to use, modify, and distribute commercially.

---

*Built with ❤️ for the global regulatory community*
