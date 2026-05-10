@echo off
setlocal enabledelayedexpansion
title GlobalRegAI — Windows Setup

echo.
echo  ==========================================
echo   GlobalRegAI - Windows Setup
echo   24/7 Free Local Regulatory AI Tool
echo  ==========================================
echo.

:: ── Check Docker ────────────────────────────────────────────
echo [1/6] Checking Docker Desktop...
docker --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Docker Desktop is not installed or not running.
    echo  Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    echo  Then restart this setup.
    pause
    exit /b 1
)
echo  Docker found.

:: ── Check Docker is running ──────────────────────────────────
docker info >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Docker Desktop is not running.
    echo  Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo  Docker is running.

:: ── Copy .env ────────────────────────────────────────────────
echo.
echo [2/6] Setting up environment...
if not exist .env (
    copy .env.example .env
    echo  Created .env from template.
    echo  NOTE: You can edit .env to change settings later.
) else (
    echo  .env already exists, skipping.
)

:: ── Pull Docker images ───────────────────────────────────────
echo.
echo [3/6] Pulling Docker images (this may take 10-20 min on first run)...
docker compose pull
if errorlevel 1 (
    echo  ERROR: Failed to pull images. Check internet connection.
    pause
    exit /b 1
)
echo  All images pulled successfully.

:: ── Start services ───────────────────────────────────────────
echo.
echo [4/6] Starting GlobalRegAI services...
docker compose up -d --remove-orphans
if errorlevel 1 (
    echo  ERROR: Failed to start services.
    pause
    exit /b 1
)
echo  Services started.

:: ── Wait for Ollama ──────────────────────────────────────────
echo.
echo [5/6] Waiting for Ollama to be ready...
:wait_ollama
timeout /t 3 /nobreak >nul
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo  Waiting for Ollama...
    goto wait_ollama
)
echo  Ollama is ready.

:: ── Pull AI Models ───────────────────────────────────────────
echo.
echo [6/6] Downloading AI models (this takes 5-15 min depending on internet)...
echo  Downloading primary model: llama3.2:3b (2GB)...
docker exec globalregai-ollama ollama pull llama3.2:3b

echo  Downloading embedding model: nomic-embed-text (274MB)...
docker exec globalregai-ollama ollama pull nomic-embed-text

echo.
echo  ==========================================
echo   Setup Complete!
echo  ==========================================
echo.
echo   Access your GlobalRegAI tools:
echo.
echo   Chat Interface  : http://localhost:3000
echo   Automation (n8n): http://localhost:5678
echo   Search Engine   : http://localhost:8080
echo   Vector DB API   : http://localhost:6333
echo.
echo   Next step: Run load-regulatory-docs.bat
echo   to load FDA/EMA/MFDS/ISO knowledge base.
echo  ==========================================
echo.

:: ── Optional: Load regulatory docs ──────────────────────────
set /p load_docs="Load regulatory knowledge base now? (y/n): "
if /i "%load_docs%"=="y" (
    call load-regulatory-docs.bat
)

pause
