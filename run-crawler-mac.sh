#!/bin/bash
echo ""
echo "=========================================="
echo " GlobalRegAI - Regulatory Data Collector"
echo " Sources: FDA/EMA/MFDS/WHO/ICH/PMDA/AEMPS"
echo "          Reddit/RAPS/PubMed/eCFR/EUR-Lex"
echo "=========================================="

cd "$(dirname "$0")"

echo ""
echo "[1/3] Installing dependencies..."
pip3 install requests beautifulsoup4 pdfplumber tqdm feedparser schedule -q

echo ""
echo "[2/3] Downloading PDF documents..."
OLLAMA_URL=http://localhost:11434 QDRANT_URL=http://localhost:6333 \
    python3 scripts/pdf_bulk_downloader.py

echo ""
echo "[3/3] Starting full data crawl..."
OLLAMA_URL=http://localhost:11434 QDRANT_URL=http://localhost:6333 \
    python3 scripts/data_crawler.py

echo ""
echo "=========================================="
echo " Data Collection Complete!"
echo "=========================================="
