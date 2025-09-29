"""
Handles translation functionality for Zoya AI Assistant
"""

import requests
import json

# Global flag to indicate if translation is available
TRANSLATOR_AVAILABLE = True

def translate_text(text, target_language):
    """
    Translate text to the target language using MyMemory API
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code
        
    Returns:
        str: Translated text or original text if failed
    """
    # If target language is English, no translation needed
    if target_language == "en":
        return text
        
    try:
        # MyMemory API endpoint
        url = "https://api.mymemory.translated.net/get"
        
        # Parameters for the translation
        params = {
            'q': text,
            'langpair': f'en|{target_language}'
        }
        
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the translated text
        translated_text = data['responseData']['translatedText']
        print(f"Translated text: {translated_text}")
        return translated_text
        
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails