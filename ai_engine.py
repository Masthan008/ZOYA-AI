"""
Handles AI responses using OpenRouter API for Zoya AI Assistant
"""

import os
import requests
from utils import stop_flag
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenRouter API
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = os.getenv("OPENROUTER_MODEL", "x-ai/grok-4-fast:free")

# Language names for prompt
language_names = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "es": "Spanish",
    "fr": "French"
}


def get_ai_response(query, language="en"):
    """
    Get AI response for the given query using OpenRouter API
    
    Args:
        query (str): User's query
        language (str): Language code for response
        
    Returns:
        str: AI response or None if failed
    """
    if not API_KEY:
        print("❌ Missing OPENROUTER_API_KEY in .env")
        return "I couldn't process that request."
        
    language_name = language_names.get(language, "English")
        
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Zoya AI Assistant"
        }

        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": f"You are Zoya, a helpful AI assistant. Respond concisely and clearly in {language_name}."},
                {"role": "user", "content": query}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            print("AI response error:", response.text)
            return "I couldn't process that request."
            
    except Exception as e:
        print("AI response error:", e)
        return "I couldn't process that request."