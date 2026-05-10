# GlobalRegAI

Free, self-hosted regulatory AI for medical devices, pharmaceuticals, cosmetics, food, GMP, and audits.

GlobalRegAI can run locally for $0 using Groq's free API tier, Docker, Open WebUI, Qdrant, SearXNG, and n8n. The repository also contains the existing public web app assets for GitHub Pages/Supabase deployment.

## 100% Free 24/7 Operating Model

| Component | Paid option | Free GlobalRegAI option |
| --- | --- | --- |
| AI model | OpenAI GPT-4 | Groq API free tier, Llama 3.3 70B |
| Server | AWS/Azure | Your computer with Docker |
| Vector database | Managed DB | Qdrant local |
| Search | Google API | SearXNG local |
| Automation | Zapier | n8n local |
| Code hosting | Paid Git hosting | GitHub public repo |
| Web deploy | Paid VM | GitHub Pages / Vercel free tier |
| Chat UI | Custom paid build | Open WebUI |

Estimated operating cost: $0 while using the local/free stack.

## Local Services

| URL | Service | Role | Cost |
| --- | --- | --- | --- |
| http://localhost:3000 | Open WebUI | Chat interface | Free |
| http://localhost:8000 | FastAPI Groq proxy | AI engine middleware | Free |
| http://localhost:5678 | n8n | Automation workflows | Free |
| http://localhost:6333 | Qdrant | RAG vector database | Free |
| http://localhost:8080 | SearXNG | Self-hosted search | Free |

## 24/7 Automation

When the computer is on, Docker keeps the stack running with `restart: unless-stopped`.

- Hourly: collect FDA recalls, EMA updates, and RSS regulatory news.
- Daily at 02:00: crawl the configured regulatory sources, store new documents in Qdrant, and refresh the knowledge base.
- Weekly on Sunday: redownload key PDFs and rebuild the vector database.

If the computer is turned off, local services stop. When it is turned back on, Docker restarts the services automatically. For always-on hosting later, the same stack can move to an always-free cloud VM such as Oracle Free Tier.

## Quick Start

1. Copy the environment example:

```bash
cp .env.example .env
```

2. Add a free Groq API key to `.env`:

```bash
GROQ_API_KEY=gsk_your_groq_api_key_here
```

3. Start all local services:

```bash
docker compose -f docker-compose.cloud.yml up -d
```

4. Open the chat UI:

```text
http://localhost:3000
```

5. Apply the system prompt once in Open WebUI:

```text
Admin Panel -> General -> System Prompt
```

Paste the contents of `config/open-webui/system_prompt.md`, then save.

## Language Coverage

| Language | Regulatory agencies |
| --- | --- |
| Korean | MFDS |
| English | FDA, EMA, TGA, Health Canada |
| Chinese | NMPA |
| Japanese | PMDA |
| Spanish | AEMPS, COFEPRIS, ANMAT, INVIMA |

## Repository Layout

| Path | Purpose |
| --- | --- |
| `scripts/llm_proxy.py` | OpenAI-compatible FastAPI proxy for Groq |
| `scripts/language_manager.py` | Language detection and terminology injection |
| `scripts/data_crawler.py` | Regulatory source crawler |
| `scripts/auto_scheduler.py` | 24/7 local automation scheduler |
| `config/open-webui/system_prompt.md` | Regulatory expert system prompt |
| `n8n-workflows/` | Importable n8n workflow JSON files |
| `src/`, `public/`, `supabase/` | Existing public web app and Supabase assets |

## GitHub / Web Deployment

The local Docker stack is the free 24/7 workstation version. The existing frontend can also be deployed from GitHub using the repository's web app files and free hosting options such as GitHub Pages or Vercel.

## License

MIT License.
