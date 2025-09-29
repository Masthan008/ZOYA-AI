#!/usr/bin/env python3
"""
Main entry point for Zoya AI Assistant
"""

import keyboard
import sys
import time

# Try to import all modules
try:
    from speech_input import get_voice_input, SR_AVAILABLE
except ImportError:
    print("Warning: speech_input module not available.")
    SR_AVAILABLE = False
    def get_voice_input(language="en"):
        return None

try:
    from speech_output import speak_text, stop_speaking
except ImportError:
    print("Warning: speech_output module not available.")
    def speak_text(text, language="en"):
        print(f"Text output: {text}")
    def stop_speaking():
        print("Speech stopped.")

try:
    from ai_engine import get_ai_response, OPENAI_AVAILABLE
except ImportError:
    print("Warning: ai_engine module not available.")
    OPENAI_AVAILABLE = False
    def get_ai_response(query, language="en"):
        return None

try:
    from duckduckgo_handler import search_web, DDGS_AVAILABLE
except ImportError:
    print("Warning: duckduckgo_handler module not available.")
    DDGS_AVAILABLE = False
    def search_web(query):
        return None

# Import translator module
try:
    from translator import translate_text
    TRANSLATOR_AVAILABLE = True
    print("Translator module imported successfully.")
except ImportError as e:
    print(f"Warning: translator module not available. Error: {e}")
    TRANSLATOR_AVAILABLE = False
    def translate_text(text, target_language):
        return text

from utils import clean_text, stop_flag, reset_stop_flag


def main():
    print("Initializing Zoya AI Assistant...")
    print("Please select your preferred language:")
    print("1. English")
    print("2. Hindi")
    print("3. Telugu")
    print("4. Tamil")
    print("5. Spanish")
    print("6. French")
    
    lang_choice = input("Enter your choice (1-6): ")
    
    language_map = {
        "1": "en",
        "2": "hi",
        "3": "te",
        "4": "ta",
        "5": "es",
        "6": "fr"
    }
    
    language_names = {
        "en": "English",
        "hi": "Hindi",
        "te": "Telugu",
        "ta": "Tamil",
        "es": "Spanish",
        "fr": "French"
    }
    
    selected_language = language_map.get(lang_choice, "en")
    selected_language_name = language_names.get(selected_language, "English")
    
    print(f"Selected language: {selected_language_name}")
    
    # Set up interrupt handler for text mode
    keyboard_listener = None
    try:
        keyboard_listener = keyboard.on_press_key("space", lambda _: stop_speaking())
    except Exception as e:
        print(f"Keyboard interrupt setup failed: {e}")
    
    print("\nType 'exit' anytime to quit.\n")
    
    while True:
        try:
            # Reset stop flag at the beginning of each conversation
            reset_stop_flag()
            
            print("\nSelect mode:")
            print("1. Voice Mode")
            print("2. Text Mode")
            print("3. Exit")
            
            mode = input("Enter your choice (1-3): ")
            
            if mode == "3":
                print("Goodbye!")
                speak_text("Goodbye! Have a great day!", selected_language)
                break
                
            if mode not in ["1", "2"]:
                print("Invalid choice. Please try again.")
                continue
                
            query = ""
            if mode == "1":
                if not SR_AVAILABLE:
                    print("Voice mode not available due to missing dependencies.")
                    continue
                print("Listening... Say something (say 'stop' to interrupt)")
                query = get_voice_input(selected_language)
                if query and query.lower() == "stop":
                    stop_speaking()
                    continue
            elif mode == "2":
                query = input("Enter your query: ").strip()
                if query.lower() in ["exit", "quit", "bye"]:
                    print("Zoya: Goodbye! Have a great day 🌸")
                    speak_text("Goodbye! Have a great day!", selected_language)
                    break
                if query.lower() == "stop":
                    stop_speaking()
                    continue
                
            if not query:
                continue
                
            print(f"You said: {query}")
            
            # Check if query is general knowledge or needs AI
            if is_general_knowledge_query(query):
                # Search web for general knowledge
                search_result = search_web(query)
                response = search_result if search_result else "I couldn't find information on that topic."
            else:
                # Use AI for complex queries
                if OPENAI_AVAILABLE:
                    ai_response = get_ai_response(query, selected_language)
                    response = ai_response if ai_response else "I couldn't process that request."
                else:
                    # Fallback to web search if AI is not available
                    search_result = search_web(query)
                    response = search_result if search_result else "I couldn't find information on that topic."
            
            # Translate response if needed
            if selected_language != "en" and TRANSLATOR_AVAILABLE:
                print(f"Translating response to {selected_language_name}...")
                response = translate_text(response, selected_language)
            
            # Clean response text
            clean_response = clean_text(response)
            
            # Speak the response
            print(f"Zoya: {clean_response}")
            speak_text(clean_response, selected_language)
            
            # Small delay to prevent rapid looping
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            speak_text("Goodbye! Have a great day!", selected_language)
            break
        except Exception as e:
            print(f"An error occurred: {e}")


def is_general_knowledge_query(query):
    """Determine if a query is general knowledge (should use web search)"""
    general_keywords = [
        "who is", "what is", "when was", "where is", "capital of", 
        "population of", "temperature in", "weather in", "current time in"
    ]
    return any(keyword in query.lower() for keyword in general_keywords)


if __name__ == "__main__":
    main()