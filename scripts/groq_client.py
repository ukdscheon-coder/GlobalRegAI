#!/usr/bin/env python3
"""
GlobalRegAI — Groq API Client
Handles high-speed inference using Groq Cloud (Llama-3.3-70b).
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional

class GroqClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")

        if not self.api_key:
            raise ValueError("ERROR: GROQ_API_KEY not found. Please set it in .env file.")

    def chat_completion(self, 
                        messages: List[Dict[str, str]], 
                        temperature: float = 0.2, 
                        max_tokens: int = 4096) -> str:
        """Sends a chat request to Groq API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"ERROR (Groq API): {str(e)}"

# 간단한 테스트 코드 (직접 실행 시)
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # .env 파일 로드
    
    client = GroqClient()
    test_messages = [
        {"role": "system", "content": "You are a regulatory expert."},
        {"role": "user", "content": "Hola, ¿puedes ayudarme con las regulaciones de AEMPS?"}
    ]
    print("\n--- Groq API Test Response ---")
    print(client.chat_completion(test_messages))
