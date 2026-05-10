#!/bin/bash
echo "[GlobalRegAI] Starting services..."
docker compose up -d
echo ""
echo "  Chat Interface  : http://localhost:3000"
echo "  Automation (n8n): http://localhost:5678"
echo "  Search Engine   : http://localhost:8080"
echo ""
open http://localhost:3000
