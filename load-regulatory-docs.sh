#!/bin/bash
echo ""
echo "[GlobalRegAI] Loading Regulatory Knowledge Base..."
echo " Sources: FDA / EMA / MFDS / ISO"
echo ""

if command -v python3 &> /dev/null; then
    pip3 install requests qdrant-client tqdm -q
    OLLAMA_URL=http://localhost:11434 QDRANT_URL=http://localhost:6333 \
        python3 scripts/ingest_regulatory_docs.py
else
    echo " Python3 not found. Running via Docker..."
    docker cp scripts/ingest_regulatory_docs.py globalregai-ollama:/tmp/
    docker exec \
        -e OLLAMA_URL=http://localhost:11434 \
        -e QDRANT_URL=http://qdrant:6333 \
        globalregai-ollama \
        sh -c "pip install requests tqdm -q && python3 /tmp/ingest_regulatory_docs.py"
fi

echo ""
echo " Knowledge base loaded!"
