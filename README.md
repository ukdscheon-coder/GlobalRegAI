# GlobalRegAI: Enterprise Regulatory SaaS

GlobalRegAI is a fully automated, cloud-based SaaS platform that provides real-time, global regulatory intelligence (FDA, EMA, MFDS, NMPA, PMDA, ISO, GMP) via a conversational AI interface. 

## Features

* **Global AI Consultant**: Search 17 global agencies instantly using OpenAI and Supabase Vector DB.
* **Freemium Paywall**: Guests receive 5 free queries before hitting a paywall to sign up.
* **PRO Enterprise Modules**: 10 specialized engines including GMP Audit, HS-Code Linkage, and Approval Timelines.
* **Automated Crawler (GitHub Actions)**: Daily cron job runs the python scraper to feed new global regulations into the Supabase Vector Database.
* **PWA Enabled**: Installable on iOS/Android and Desktop directly from the browser.
* **Markdown Rendering**: AI responses are formatted precisely like Google's AI Overviews for maximum readability.

## Architecture
- **Frontend**: React, Vite, TypeScript, Lucide Icons, React Markdown
- **Backend/DB**: Supabase (PostgreSQL + pgvector), Edge Functions
- **Inference**: OpenAI (gpt-4o-mini)
- **Deployment**: GitHub Pages (UI), Supabase Cloud (API)

## Deployment Instructions
To manually deploy updates to the frontend:
```bash
npm run deploy
```
To update the cloud AI engine:
```bash
npx supabase functions deploy chat --no-verify-jwt
```
