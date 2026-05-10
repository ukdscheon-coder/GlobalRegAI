#!/bin/bash
# ============================================================
#  GlobalRegAI — macOS Setup Script
#  Works on: Intel Mac & Apple Silicon (M1/M2/M3/M4)
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}=========================================="
echo " GlobalRegAI - macOS Setup"
echo " 24/7 Free Local Regulatory AI Tool"
echo -e "==========================================${NC}"
echo ""

# ── Check Architecture ───────────────────────────────────────
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    echo -e "${GREEN}  Apple Silicon (M-series) detected — GPU acceleration enabled${NC}"
else
    echo -e "${YELLOW}  Intel Mac detected${NC}"
fi

# ── Check Docker ─────────────────────────────────────────────
echo ""
echo "[1/6] Checking Docker Desktop..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}  ERROR: Docker Desktop is not installed.${NC}"
    echo "  Please install from: https://www.docker.com/products/docker-desktop/"
    echo ""
    echo "  Apple Silicon: download the 'Apple Silicon' version"
    echo "  Intel Mac:     download the 'Intel Chip' version"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}  ERROR: Docker Desktop is not running.${NC}"
    echo "  Please open Docker Desktop from Applications and try again."
    exit 1
fi
echo -e "${GREEN}  Docker is running.${NC}"

# ── Setup .env ───────────────────────────────────────────────
echo ""
echo "[2/6] Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}  Created .env from template.${NC}"
else
    echo "  .env already exists, skipping."
fi

# ── Apple Silicon: remove GPU deploy section for compatibility
if [ "$ARCH" = "arm64" ]; then
    echo "  Apple Silicon: Metal GPU will be used automatically by Ollama."
fi

# ── Pull Docker images ───────────────────────────────────────
echo ""
echo "[3/6] Pulling Docker images (10-20 min on first run)..."
docker compose pull
echo -e "${GREEN}  All images pulled.${NC}"

# ── Start services ───────────────────────────────────────────
echo ""
echo "[4/6] Starting GlobalRegAI services..."
docker compose up -d --remove-orphans
echo -e "${GREEN}  Services started.${NC}"

# ── Wait for Ollama ──────────────────────────────────────────
echo ""
echo "[5/6] Waiting for Ollama to be ready..."
until curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
    echo "  Waiting for Ollama..."
    sleep 3
done
echo -e "${GREEN}  Ollama is ready.${NC}"

# ── Pull AI Models ───────────────────────────────────────────
echo ""
echo "[6/6] Downloading AI models..."
echo "  Downloading primary model: llama3.2:3b (2GB)..."
docker exec globalregai-ollama ollama pull llama3.2:3b

echo "  Downloading embedding model: nomic-embed-text (274MB)..."
docker exec globalregai-ollama ollama pull nomic-embed-text

echo ""
echo -e "${GREEN}=========================================="
echo " Setup Complete!"
echo -e "==========================================${NC}"
echo ""
echo " Access your GlobalRegAI tools:"
echo ""
echo -e "  Chat Interface  : ${BLUE}http://localhost:3000${NC}"
echo -e "  Automation (n8n): ${BLUE}http://localhost:5678${NC}"
echo -e "  Search Engine   : ${BLUE}http://localhost:8080${NC}"
echo -e "  Vector DB API   : ${BLUE}http://localhost:6333${NC}"
echo ""
echo " Next step: run ./load-regulatory-docs.sh"
echo " to load FDA/EMA/MFDS/ISO knowledge base."
echo ""

# ── Offer to load docs ───────────────────────────────────────
read -p " Load regulatory knowledge base now? (y/n): " load_docs
if [ "$load_docs" = "y" ] || [ "$load_docs" = "Y" ]; then
    chmod +x load-regulatory-docs.sh
    ./load-regulatory-docs.sh
fi

# ── Auto-open browser ────────────────────────────────────────
open http://localhost:3000
