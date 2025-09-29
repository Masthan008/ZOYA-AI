"""
Handles translation functionality for Zoya AI Assistant
"""

import requests
import json

# Global flag to indicate if translation is available
TRANSLATOR_AVAILABLE = True

# Language code mapping for the translate library
LANGUAGE_MAP = {
    "en": "EN",
    "hi": "HI",
    "te": "TE",  # Note: The translate library might not support all languages
    "ta": "TA",  # Note: The translate library might not support all languages
    "es": "ES",
    "fr": "FR"
}


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
        
    # Check if text is too long for translation
    if len(text) > 500:
        # Split text into smaller chunks
        chunks = [text[i:i+400] for i in range(0, len(text), 400)]
        translated_chunks = []
        for chunk in chunks:
            translated_chunk = translate_chunk(chunk, target_language)
            if translated_chunk:
                translated_chunks.append(translated_chunk)
        return " ".join(translated_chunks) if translated_chunks else text
    
    return translate_chunk(text, target_language)


def translate_chunk(text, target_language):
    """
    Translate a single chunk of text
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code
        
    Returns:
        str: Translated text or original text if failed
    """
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
        
        # Handle error responses
        if "QUERY LENGTH LIMIT EXCEEDED" in translated_text:
            print(f"Translation error: {translated_text}")
            return text
            
        print(f"Translated text: {translated_text}")
        return translated_text
        
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails