# GlobalRegAI 🏥

**24/7 Free Local AI for Global Regulatory Affairs**

의료기기 · 의약품 · 화장품 · 식품 인허가 · GMP · Audit 전문 AI

---

## What is GlobalRegAI?

GlobalRegAI is a 100% free, offline-capable AI tool for regulatory professionals.
Built on open-source components — no subscriptions, no API keys, no data leaves your computer.

**Regulatory Coverage:**
- 🇺🇸 FDA (21 CFR 820, 21 CFR 211, FSMA, 510(k), PMA, NDA)
- 🇪🇺 EMA / EU MDR / EU GMP Guidelines
- 🇰🇷 MFDS (식품의약품안전처) 의료기기·의약품·화장품·식품
- 🌍 ISO 13485, ISO 14971, IEC 62304, ICH Q8-Q11

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   YOUR COMPUTER                      │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  Ollama  │  │Open WebUI│  │       n8n        │  │
│  │  (LLM)   │◄─│  (Chat)  │  │  (Automation)    │  │
│  │ :11434   │  │  :3000   │  │     :5678        │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│       ▲                            │                │
│       │        ┌──────────┐        ▼                │
│       │        │  Qdrant  │  ┌──────────┐           │
│       └────────│ (Vector  │  │ SearXNG  │           │
│   (RAG/embed)  │   DB)    │  │ (Search) │           │
│                │  :6333   │  │  :8080   │           │
│                └──────────┘  └──────────┘           │
└─────────────────────────────────────────────────────┘
```

| Component | Role | Port |
|-----------|------|------|
| **Ollama** | Run AI models locally | 11434 |
| **Open WebUI** | Chat interface (like ChatGPT) | 3000 |
| **n8n** | Workflow automation | 5678 |
| **Qdrant** | Vector DB for RAG | 6333 |
| **SearXNG** | Self-hosted web search | 8080 |

---

## Prerequisites (What You Need to Install First)

### Step 1 — Install Docker Desktop

Docker is the only software you need to install manually.

**Windows:**
1. Go to: https://www.docker.com/products/docker-desktop/
2. Click **"Download for Windows"**
3. Run the installer and restart your computer
4. Open Docker Desktop from the Start menu — wait for it to say **"Docker Desktop is running"**

**macOS (Apple Silicon M1/M2/M3/M4):**
1. Go to: https://www.docker.com/products/docker-desktop/
2. Click **"Download for Mac — Apple Silicon"**
3. Drag Docker to Applications folder
4. Open Docker from Applications — wait for the whale icon in the menu bar to stop animating

**macOS (Intel):**
1. Same URL — click **"Download for Mac — Intel Chip"**
2. Same installation steps

> Minimum requirements: 8GB RAM, 20GB free disk space

---

## Installation

### Windows

```batch
# 1. Open File Explorer → go to C:\Users\laser\GlobalRegAI\
# 2. Double-click setup-windows.bat
# 3. Follow the prompts (takes 15-30 min on first run)
```

Or from Command Prompt:
```batch
cd C:\Users\laser\GlobalRegAI
setup-windows.bat
```

### macOS

```bash
# 1. Open Terminal
# 2. Navigate to the GlobalRegAI folder
cd ~/GlobalRegAI   # or wherever you saved this folder

# 3. Make scripts executable
chmod +x setup-mac.sh start-mac.sh stop-mac.sh load-regulatory-docs.sh

# 4. Run setup
./setup-mac.sh
```

---

## Daily Use

### Start GlobalRegAI

**Windows:** Double-click `start-windows.bat`

**Mac:** 
```bash
./start-mac.sh
```

Then open your browser: **http://localhost:3000**

### Stop GlobalRegAI

**Windows:** Double-click `stop-windows.bat`

**Mac:**
```bash
./stop-mac.sh
```

---

## Setup System Prompt (One-time, 5 minutes)

After starting, configure the AI persona:

1. Open **http://localhost:3000**
2. Click the **gear icon** (Settings) → **Admin Panel**
3. Go to **General** → **System Prompt**
4. Open `config/open-webui/system_prompt.md`
5. Copy the entire content and paste into the System Prompt field
6. Click **Save**

Now GlobalRegAI knows it's a regulatory expert.

---

## Load Regulatory Knowledge Base (One-time, 10 minutes)

This loads FDA/EMA/MFDS/ISO knowledge so the AI can answer with accurate citations.

**Windows:**
```batch
load-regulatory-docs.bat
```

**Mac:**
```bash
./load-regulatory-docs.sh
```

> **Requirements:** Python 3.8+ OR Docker must be running
> Install Python from: https://www.python.org/downloads/

---

## What You Can Ask GlobalRegAI

### Medical Device Regulatory

```
What documents do I need for FDA 510(k) submission?

Create a gap analysis checklist for ISO 13485:2016 for 
a Class II medical device manufacturer.

What are the GSPR (General Safety and Performance Requirements) 
for EU MDR 2017/745?

한국 의료기기 2등급 허가를 위한 기술문서 목록을 알려주세요.
```

### GMP Audit

```
Generate a GMP audit checklist for a pharmaceutical 
tablet manufacturing facility (FDA 21 CFR 211).

I received a Major finding: "Training records are not current 
for 3 operators." Write a CAPA response.

What are the top 10 FDA 483 observations for medical device companies?
```

### Pharmaceutical

```
Explain ICH Q10 Pharmaceutical Quality System requirements.

What is the difference between NDA and ANDA submissions?

How do I prepare for an EU GMP inspection?

ICH Q8, Q9, Q10의 핵심 요구사항을 설명해주세요.
```

### Cosmetics & Food

```
What are FDA requirements for cosmetic labeling in the US?

Explain FSMA Preventive Controls for Human Food requirements.

EU 화장품 규정에서 금지 성분 목록은 어디서 확인하나요?
```

---

## Automation Workflows (n8n)

Access the automation dashboard: **http://localhost:5678**

### Available Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| GMP Audit Checklist | `POST /webhook/gmp-audit` | Generate custom audit checklists |
| Daily Regulatory Updates | Every day 9AM | Fetch latest FDA recalls/enforcement |
| CAPA Report Generator | `POST /webhook/generate-capa` | Write complete CAPA reports |

### Import Workflows

1. Open **http://localhost:5678**
2. Click **Workflows** → **Import from file**
3. Import each `.json` file from `n8n-workflows/` folder

### Test CAPA Generator

```bash
curl -X POST http://localhost:5678/webhook/generate-capa \
  -H "Content-Type: application/json" \
  -d '{
    "finding_type": "Documentation",
    "description": "Batch records missing operator signatures on 5 production steps",
    "area": "Production",
    "framework": "FDA 21 CFR Part 820",
    "classification": "Major"
  }'
```

---

## AI Models

Default model: **llama3.2:3b** (2GB, good for most questions)

### Upgrade for Better Quality

In Open WebUI, go to the model selector and download:

| Model | Size | Best For |
|-------|------|----------|
| `llama3.2:1b` | 800MB | Fast responses, basic Q&A |
| `llama3.2:3b` | 2GB | **Recommended** — good balance |
| `llama3.1:8b` | 4.7GB | Better reasoning, complex docs |
| `llama3.1:70b` | 40GB | Best quality (needs 48GB+ RAM) |
| `mistral:7b` | 4GB | Good for technical writing |
| `qwen2.5:7b` | 4.7GB | Excellent multilingual (Korean/Chinese) |

To download a new model:
```bash
# In terminal while services are running:
docker exec globalregai-ollama ollama pull qwen2.5:7b
```

---

## Uploading Your Own Regulatory Documents

You can upload your own SOPs, specifications, and guidelines for Q&A:

1. Open **http://localhost:3000**
2. Click the **📎 paperclip icon** in the chat
3. Upload PDF, Word, or text files
4. Ask questions about the uploaded document

GlobalRegAI will answer based on your uploaded documents.

---

## Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker info

# Check service status
docker compose ps

# View logs
docker compose logs ollama
docker compose logs open-webui
```

### Ollama is slow
- For Apple Silicon: Metal GPU is used automatically — no action needed
- For Windows NVIDIA GPU: ensure NVIDIA Container Toolkit is installed
- For CPU-only: use smaller models (`llama3.2:1b`)

### "Connection refused" error
Make sure Docker Desktop is running before starting GlobalRegAI.

### Reset everything
```bash
docker compose down -v  # WARNING: deletes all data
docker compose up -d
```

---

## Regulatory Intelligence Sources

GlobalRegAI is pre-loaded with knowledge from these public sources:

| Agency | Source |
|--------|--------|
| FDA | https://www.fda.gov/regulatory-information |
| EMA | https://www.ema.europa.eu/en/documents |
| MFDS | https://www.mfds.go.kr/eng |
| ISO | https://www.iso.org (public summaries) |
| ICH | https://www.ich.org/page/quality-guidelines |
| FDA API | https://api.fda.gov (real-time recalls/enforcement) |

---

## Privacy & Security

- ✅ 100% local — no data sent to any cloud service
- ✅ Works offline (after initial model download)
- ✅ Your regulatory documents stay on your computer
- ✅ No API keys required
- ✅ No usage limits

---

## License

GlobalRegAI is built entirely on open-source components:
- [Ollama](https://github.com/ollama/ollama) — MIT License
- [Open WebUI](https://github.com/open-webui/open-webui) — MIT License
- [n8n](https://github.com/n8n-io/n8n) — Sustainable Use License (free for personal use)
- [Qdrant](https://github.com/qdrant/qdrant) — Apache 2.0 License
- [SearXNG](https://github.com/searxng/searxng) — AGPL-3.0 License

---

## Disclaimer

GlobalRegAI provides regulatory information for educational and reference purposes.
For official regulatory submissions, product approvals, and compliance decisions,
always consult a licensed regulatory affairs professional and verify information
with the relevant regulatory authority.

---

*Built for global regulatory professionals — free, private, powerful.*
