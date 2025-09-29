"""
Handles speech-to-text functionality for Zoya AI Assistant
"""

from utils import stop_flag

# Try to import speech_recognition
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    print("Warning: speech_recognition not available. Voice input will be disabled.")
    SR_AVAILABLE = False


def get_voice_input(language="en"):
    """
    Capture voice input from microphone and convert to text
    
    Args:
        language (str): Language code for speech recognition
        
    Returns:
        str: Transcribed text or None if failed
    """
    if not SR_AVAILABLE:
        print("Speech recognition not available.")
        return None
        
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing...")
            
            # Language mapping for speech recognition
            lang_map = {
                "en": "en-US",
                "hi": "hi-IN",
                "te": "te-IN",
                "ta": "ta-IN",
                "es": "es-ES",
                "fr": "fr-FR"
            }
            
            language_code = lang_map.get(language, "en-US")
            
            text = recognizer.recognize_google(audio, language=language_code)
            return text
            
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None