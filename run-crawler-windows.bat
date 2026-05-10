@echo off
title GlobalRegAI — Data Crawler

echo.
echo  ==========================================
echo   GlobalRegAI - Regulatory Data Collector
echo   Sources: FDA / EMA / MFDS / WHO / ICH
echo            PIC/S / PMDA / NMPA / AEMPS
echo            Reddit / RAPS / PubMed / eCFR
echo  ==========================================
echo.

cd /d C:\Users\laser\GlobalRegAI

echo [1/3] Installing dependencies...
pip install requests beautifulsoup4 pdfplumber tqdm feedparser schedule -q

echo.
echo [2/3] Downloading PDF documents...
set OLLAMA_URL=http://localhost:11434
set QDRANT_URL=http://localhost:6333
python scripts\pdf_bulk_downloader.py

echo.
echo [3/3] Starting full data crawl...
python scripts\data_crawler.py

echo.
echo  ==========================================
echo   Data Collection Complete!
echo   Knowledge base updated in Qdrant DB.
echo  ==========================================
pause
