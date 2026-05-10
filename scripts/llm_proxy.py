#!/usr/bin/env python3
"""
GlobalRegAI ??LLM Intelligence Proxy
Acts as an OpenAI-compatible API that adds multilingual intelligence.
"""

import os
import sys
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from groq_client import GroqClient
from language_manager import LanguageManager
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GlobalRegAI Proxy")
groq_client = GroqClient()
lang_manager = LanguageManager()

@app.post("/v1/chat/completions")
async def chat_proxy(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    
    if not messages:
        raise HTTPException(status_code=400, detail="Messages are required")

    # 1. 留덉?留??ъ슜??吏덈Ц 異붿텧
    user_content = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            user_content = msg["content"]
            break
    
    # 2. ?몄뼱 媛먯? 諛?洹쒖젙 ?⑹뼱吏?濡쒕뱶
    lang_code = lang_manager.detect_language(user_content)
    system_addon = lang_manager.get_system_prompt_addon(lang_code)
    
    # 3. ?쒖뒪???꾨＼?꾪듃 ?낅뜲?댄듃 ?먮뒗 ?쎌엯
    has_system = False
    for msg in messages:
        if msg["role"] == "system":
            msg["content"] = msg["content"] + "\n" + system_addon
            has_system = True
            break
    
    if not has_system:
        messages.insert(0, {"role": "system", "content": system_addon})

    # 4. Groq API ?몄텧
    print(f"[Proxy] Detected language: {lang_code}. Calling Groq...")
    response_content = groq_client.chat_completion(
        messages=messages,
        temperature=body.get("temperature", 0.2),
        max_tokens=body.get("max_tokens", 4096)
    )

    # 5. OpenAI ?명솚 ?묐떟 ?앹꽦
    return {
        "id": "globalregai-proxy-id",
        "object": "chat.completion",
        "created": 123456789,
        "model": groq_client.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_content
                },
                "finish_reason": "stop"
            }
        ]
    }

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "globalregai-llama3-70b", "object": "model", "owned_by": "globalregai"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


