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

# 🧠 Persistent memory (list of messages)
chat_memory = [
    {"role": "system", "content": "You are Zoya, a helpful AI assistant. Remember the user's previous context and respond concisely and clearly."}
]


def get_ai_response(query, language="en"):
    """
    Get AI response for the given query using OpenRouter API with memory context
    
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

        # 🧠 Add user query to memory
        chat_memory.append({"role": "user", "content": query})

        # Update system message with language context
        system_message = f"You are Zoya, a helpful AI assistant. Respond concisely and clearly in {language_name}. Remember the user's previous context."
        
        # Find and update the system message in chat_memory
        for msg in chat_memory:
            if msg["role"] == "system":
                msg["content"] = system_message
                break
        else:
            # If no system message found, add one
            chat_memory.insert(0, {"role": "system", "content": system_message})

        data = {
            "model": MODEL_NAME,
            "messages": chat_memory
        }

        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            ai_reply = result["choices"][0]["message"]["content"].strip()

            # 🧠 Save AI response in memory
            chat_memory.append({"role": "assistant", "content": ai_reply})

            return ai_reply
        else:
            print("AI response error:", response.text)
            return "I couldn't process that request."
            
    except Exception as e:
        print("AI response error:", e)
        return "I couldn't process that request."


def clear_memory():
    """Clear the chat memory, keeping only the system message"""
    global chat_memory
    system_msg = chat_memory[0] if chat_memory and chat_memory[0]["role"] == "system" else {
        "role": "system", 
        "content": "You are Zoya, a helpful AI assistant. Remember the user's previous context and respond concisely and clearly."
    }
    chat_memory = [system_msg]