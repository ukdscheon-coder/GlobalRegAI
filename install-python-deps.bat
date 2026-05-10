@echo off
title GlobalRegAI — Python Dependencies

echo.
echo [GlobalRegAI] Installing Python dependencies...
echo.

pip install requests beautifulsoup4 pdfplumber tqdm feedparser schedule qdrant-client lxml -q

echo.
echo Done! All dependencies installed.
pause
