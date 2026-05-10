@echo off
title GlobalRegAI — Load Regulatory Knowledge Base

echo.
echo [GlobalRegAI] Loading Regulatory Knowledge Base...
echo  Sources: FDA / EMA / MFDS / ISO
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  Python not found. Running via Docker...
    docker exec globalregai-ollama sh -c "pip install requests tqdm >/dev/null 2>&1 || true"
    docker cp scripts\ingest_regulatory_docs.py globalregai-ollama:/tmp/
    docker exec -e OLLAMA_URL=http://localhost:11434 -e QDRANT_URL=http://qdrant:6333 globalregai-ollama python3 /tmp/ingest_regulatory_docs.py
) else (
    pip install requests qdrant-client tqdm -q
    set OLLAMA_URL=http://localhost:11434
    set QDRANT_URL=http://localhost:6333
    python scripts\ingest_regulatory_docs.py
)

echo.
echo  Knowledge base loaded successfully!
pause
