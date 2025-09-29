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
except ImportError as e:
    print(f"❌ Error loading speech_input: {e}")
    SR_AVAILABLE = False
    def get_voice_input(language="en"):
        return None

try:
    from speech_output import speak_text, stop_speaking
except ImportError as e:
    print(f"❌ Error loading speech_output: {e}")
    def speak_text(text, language="en"):
        print(f"Text output: {text}")
    def stop_speaking():
        print("Speech stopped.")

try:
    from ai_engine import get_ai_response, clear_memory
    # Check if OPENAI_AVAILABLE is defined, if not define it
    try:
        from ai_engine import OPENAI_AVAILABLE
    except ImportError:
        OPENAI_AVAILABLE = False
except ImportError as e:
    print(f"❌ Error loading ai_engine: {e}")
    OPENAI_AVAILABLE = False
    def get_ai_response(query, language="en"):
        return None
    def clear_memory():
        pass

try:
    from duckduckgo_handler import search_web, DDGS_AVAILABLE
except ImportError as e:
    print(f"❌ Error loading duckduckgo_handler: {e}")
    DDGS_AVAILABLE = False
    def search_web(query):
        return None

# Import translator module
try:
    from translator import translate_text
    TRANSLATOR_AVAILABLE = True
    print("Translator module imported successfully.")
except ImportError as e:
    print(f"❌ Error loading translator: {e}")
    TRANSLATOR_AVAILABLE = False
    def translate_text(text, target_language):
        return text

# Import logger module
try:
    from logger import log_interaction
    LOGGER_AVAILABLE = True
    print("Logger module imported successfully.")
except ImportError as e:
    print(f"❌ Error loading logger: {e}")
    LOGGER_AVAILABLE = False
    def log_interaction(user_query, ai_reply, mode="text", search_result=None):
        pass

from utils import clean_text, stop_flag, reset_stop_flag


def main():
    print("✨ Hello! I'm Zoya — your smart personal AI assistant ✨")
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
    
    # Main loop for mode selection
    while True:
        print("\nSelect mode:")
        print("1. Voice Mode (AI)")
        print("2. Text Mode (AI)")
        print("3. Live Search Mode 🌐 (DuckDuckGo)")
        print("4. Clear Memory")
        print("5. Exit")
        
        mode = input("Enter your choice (1-5): ")
        
        if mode == "1":
            start_voice_mode(selected_language, selected_language_name)
        elif mode == "2":
            start_text_mode(selected_language, selected_language_name)
        elif mode == "3":
            start_live_search_mode(selected_language, selected_language_name)
        elif mode == "4":
            clear_memory()
            print("🧠 Zoya's memory cleared.")
            speak_text("My memory has been cleared.", selected_language)
        elif mode == "5":
            print("👋 Exiting Zoya. Goodbye!")
            speak_text("Goodbye! Have a nice day!", selected_language)
            break
        else:
            print("Invalid choice. Please try again.")


def start_text_mode(selected_language, selected_language_name):
    """Start text mode conversation loop"""
    print(f"\n🧠 Zoya Mode: Text (AI) - {selected_language_name}")
    print("Type 'exit' to quit, or 'stop' to reset conversation.\n")
    
    while True:
        try:
            # Reset stop flag at the beginning of each conversation
            reset_stop_flag()
            
            query = input("Enter your query: ").strip()
            if not query:
                continue

            # 🛑 Stop Command
            if query.lower() == "stop":
                print("🧠 Zoya: Conversation reset. Let's start fresh!")
                speak_text("Conversation reset. Let's start fresh!", selected_language)
                clear_memory()
                print("💬 You can ask me another question or type 'stop' anytime.\n")
                continue  # ✅ ask again

            # ❌ Exit Command
            if query.lower() in ["exit", "quit", "bye"]:
                print("Zoya: Goodbye! 👋")
                speak_text("Goodbye! Have a nice day!", selected_language)
                break

            # 🧍 Personal Q&A
            personal_qa = {
                "what is your name": "My name is Zoya, your personal AI assistant.",
                "who created you": "I was created by Masthan Valli — my brilliant developer.",
                "who are you": "I'm Zoya, your friendly AI assistant built to help you.",
                "who made you": "Masthan Valli built me using Python and AI.",
                "who is masthan valli": "Masthan Valli is my creator — a talented developer.",
                "who developed you": "Masthan Valli developed me with love and code."
            }

            query_lower = query.lower().strip(" ?")
            if query_lower in personal_qa:
                response = personal_qa[query_lower]
            else:
                # Check if query is general knowledge or needs AI
                if is_general_knowledge_query(query):
                    # Search web for general knowledge
                    search_result = search_web(query)
                    response = search_result if search_result else "I couldn't find information on that topic."
                    
                    # Log the interaction with search result
                    if LOGGER_AVAILABLE:
                        log_interaction(user_query=query, ai_reply=response, mode="text", search_result=search_result)
                else:
                    # Use AI for complex queries
                    if OPENAI_AVAILABLE:
                        ai_response = get_ai_response(query, selected_language)
                        response = ai_response if ai_response else "I couldn't process that request."
                        
                        # Log the interaction
                        if LOGGER_AVAILABLE:
                            log_interaction(user_query=query, ai_reply=response, mode="text")
                    else:
                        # Fallback to web search if AI is not available
                        search_result = search_web(query)
                        response = search_result if search_result else "I couldn't find information on that topic."
                        
                        # Log the interaction with search result
                        if LOGGER_AVAILABLE:
                            log_interaction(user_query=query, ai_reply=response, mode="text", search_result=search_result)

            # Translate response if needed
            if selected_language != "en" and TRANSLATOR_AVAILABLE:
                print(f"Translating response to {selected_language_name}...")
                response = translate_text(response, selected_language)

            # Clean response text
            clean_response = clean_text(response)

            # Speak the response (only once)
            print(f"Zoya: {clean_response}")
            speak_text(clean_response, selected_language)
            
            # Friendly prompt after answer
            print("💬 You can ask me another question or type 'stop' anytime.\n")
            
            # Small delay to ensure speech finishes before next prompt
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\nZoya: Goodbye! 👋")
            speak_text("Goodbye! Have a nice day!", selected_language)
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Continuing to next query...")


def start_voice_mode(selected_language, selected_language_name):
    """Start voice mode conversation loop"""
    if not SR_AVAILABLE:
        print("Voice mode not available due to missing dependencies.")
        return
        
    print(f"\n🎙️ Zoya Mode: Voice (AI) - {selected_language_name}")
    print("Say 'exit' to quit, or 'stop' to reset conversation.\n")
    
    while True:
        try:
            # Reset stop flag at the beginning of each conversation
            reset_stop_flag()
            
            print("Listening... Say something (say 'stop' to interrupt or reset)")
            query = get_voice_input(selected_language)
            
            if not query:
                continue
                
            # 🛑 Stop Command
            if query.lower() == "stop":
                print("🛑 Conversation reset.")
                speak_text("Conversation reset. Let's start fresh!", selected_language)
                clear_memory()
                print("💬 You can ask me another question or say 'stop' anytime.\n")
                continue

            # ❌ Exit Command
            if query.lower() in ["exit", "quit", "bye"]:
                print("Zoya: Goodbye! 👋")
                speak_text("Goodbye! Have a nice day!", selected_language)
                break

            # 🧍 Personal Q&A
            personal_qa = {
                "what is your name": "My name is Zoya, your personal AI assistant.",
                "who created you": "I was created by Masthan Valli — my brilliant developer.",
                "who are you": "I'm Zoya, your friendly AI assistant built to help you.",
                "who made you": "Masthan Valli built me using Python and AI.",
                "who is masthan valli": "Masthan Valli is my creator — a talented developer.",
                "who developed you": "Masthan Valli developed me with love and code."
            }

            query_lower = query.lower().strip(" ?")
            if query_lower in personal_qa:
                response = personal_qa[query_lower]
            else:
                # Check if query is general knowledge or needs AI
                if is_general_knowledge_query(query):
                    # Search web for general knowledge
                    search_result = search_web(query)
                    response = search_result if search_result else "I couldn't find information on that topic."
                    
                    # Log the interaction with search result
                    if LOGGER_AVAILABLE:
                        log_interaction(user_query=query, ai_reply=response, mode="voice", search_result=search_result)
                else:
                    # Use AI for complex queries
                    if OPENAI_AVAILABLE:
                        ai_response = get_ai_response(query, selected_language)
                        response = ai_response if ai_response else "I couldn't process that request."
                        
                        # Log the interaction
                        if LOGGER_AVAILABLE:
                            log_interaction(user_query=query, ai_reply=response, mode="voice")
                    else:
                        # Fallback to web search if AI is not available
                        search_result = search_web(query)
                        response = search_result if search_result else "I couldn't find information on that topic."
                        
                        # Log the interaction with search result
                        if LOGGER_AVAILABLE:
                            log_interaction(user_query=query, ai_reply=response, mode="voice", search_result=search_result)

            # Translate response if needed
            if selected_language != "en" and TRANSLATOR_AVAILABLE:
                print(f"Translating response to {selected_language_name}...")
                response = translate_text(response, selected_language)

            # Clean response text
            clean_response = clean_text(response)

            # Speak the response (only once)
            print(f"Zoya: {clean_response}")
            speak_text(clean_response, selected_language)
            
            # Small delay to ensure speech finishes before next prompt
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\nZoya: Goodbye! 👋")
            speak_text("Goodbye! Have a nice day!", selected_language)
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Continuing to next query...")


def start_live_search_mode(selected_language, selected_language_name):
    """Start live search mode using DuckDuckGo"""
    print(f"\n🌐 Zoya Mode: Live (DuckDuckGo) - {selected_language_name}")
    print("Type 'exit' anytime to quit.\n")
    
    while True:
        try:
            query = input("🔎 Enter your search query: ").strip()
            if not query:
                continue

            if query.lower() in ["exit", "quit"]:
                print("Zoya: Exiting live mode.")
                speak_text("Exiting live mode.", selected_language)
                break

            print(f"You searched: {query}")
            result = search_web(query)
            if not result:
                result = "I couldn't find information on that topic."
            
            print(f"\nZoya (Live): {result}")
            speak_text(result, selected_language)

            # Log search
            if LOGGER_AVAILABLE:
                log_interaction(query, result, mode="live", search_result=result)
                
            # Friendly prompt after answer
            print("💬 You can search for another topic or type 'exit' to quit.\n")
                
            # Small delay to ensure speech finishes before next prompt
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\nZoya: Exiting live mode.")
            speak_text("Exiting live mode.", selected_language)
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Continuing to next query...")


def is_general_knowledge_query(query):
    """Determine if a query is general knowledge (should use web search)"""
    general_keywords = [
        "who is", "what is", "when was", "where is", "capital of", 
        "population of", "temperature in", "weather in", "current time in"
    ]
    return any(keyword in query.lower() for keyword in general_keywords)


if __name__ == "__main__":
    main()