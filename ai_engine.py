"""
Handles AI responses using OpenRouter API for Zoya AI Assistant
"""

import os
from utils import stop_flag

# Try to import openai and dotenv
try:
    import openai
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
    OPENAI_AVAILABLE = True
    
    # Configure OpenRouter API
    openai.api_base = "https://openrouter.ai/api/v1"
    openai.api_key = os.getenv("OPENROUTER_API_KEY")  # Load API key from .env file
    MODEL_NAME = os.getenv("OPENROUTER_MODEL", "x-ai/grok-4-fast:free")  # Load model from .env or use default
except ImportError:
    print("Warning: openai or dotenv not available. AI functionality will be disabled.")
    OPENAI_AVAILABLE = False
    MODEL_NAME = "x-ai/grok-4-fast:free"

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
    if not OPENAI_AVAILABLE:
        return None
        
    language_name = language_names.get(language, "English")
        
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": f"You are Zoya, a helpful AI assistant. Respond concisely and clearly in {language_name}."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"AI response error: {e}")
        return None