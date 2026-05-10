#!/usr/bin/env python3
"""
GlobalRegAI ??Language Manager & Terminology Injector
Detects user language and injects specific regulatory glossary.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional

class LanguageManager:
    def __init__(self, config_path: str = "config/languages/language_config.json"):
        self.base_path = Path(os.getenv("APP_BASE_PATH", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.config_path = self.base_path / config_path
        self.config = self._load_json(self.config_path)
        self.languages = {lang["code"]: lang for lang in self.config.get("supported_languages", [])}

    def _load_json(self, path: Path) -> Dict:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _load_file(self, filename: str) -> str:
        path = self.base_path / "config/languages" / filename
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def detect_language(self, text: str) -> str:
        """Detects language based on character script and keywords."""
        # Simple heuristic detection
        if re.search(r"[\uac00-\ud7a3]", text): return "ko"    # Hangul
        if re.search(r"[\u3040-\u309f\u30a0-\u30ff]", text): return "ja" # Hiragana/Katakana
        
        # Check for Spanish specific characters or common words
        spanish_indicators = r"[쩔징]|찼|챕|챠|처|첬|챰"
        if re.search(spanish_indicators, text, re.IGNORECASE): return "es"
        
        # Fallback to English if it's primarily Latin without Spanish indicators
        # In a real app, you'd use a library like langdetect here.
        return "en"

    def get_system_prompt_addon(self, lang_code: str) -> str:
        """Generates the system prompt instructions for the specific language."""
        lang_info = self.languages.get(lang_code)
        if not lang_info:
            lang_info = self.languages.get("en") # Fallback to English

        terminology = self._load_file(lang_info["terminology_file"])
        
        addon = f"""
### Language and Regulatory Persona Instructions
- **Response Language**: {lang_info['name']}
- **Regulatory Context**: {lang_info['regulatory_context']}
- **Tone/Style**: {lang_info['response_style']}
- **Target Agencies**: {json.dumps(lang_info['agencies'], ensure_ascii=False)}

### Mandatory Regulatory Terminology ({lang_info['code'].upper()})
You MUST use the professional terminology from the following glossary when responding in {lang_info['name']}:
{terminology}

Ensure all agency names and legal terms strictly follow the standards above.
"""
        return addon

# ?뚯뒪??肄붾뱶
if __name__ == "__main__":
    mgr = LanguageManager()
    
    test_texts = [
        "쩔C처mo puedo registrar un dispositivo m챕dico en la AEMPS?",
        "MFDS ?섎즺湲곌린 ?덇? ?덉감瑜??뚮젮以?",
        "FDA??GMP 媛먯궗 ??ぉ? 臾댁뾿?멸???"
    ]
    
    for text in test_texts:
        lang = mgr.detect_language(text)
        print(f"\n[Detected: {lang}] Input: {text}")
        # print(mgr.get_system_prompt_addon(lang)) # ?꾩껜 ?꾨＼?꾪듃 ?뺤씤??
