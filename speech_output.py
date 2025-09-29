"""
Handles text-to-speech functionality for Zoya AI Assistant with stop control
"""

import threading
import time
import os
import re
import pyttsx3
from gtts import gTTS
import pygame
import keyboard
from utils import stop_flag

# Try to import pyttsx3
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    print("Warning: pyttsx3 not available. Will use gTTS only.")
    PYTTSX3_AVAILABLE = False

# Try to import gTTS and pygame
try:
    from gtts import gTTS
    import pygame
    GTTS_AVAILABLE = True
except ImportError:
    print("Warning: gTTS or pygame not available. Speech output may be limited.")
    GTTS_AVAILABLE = False

# Global variables for speech control
engine = None
is_speaking = False


def clean_text(text):
    """
    Clean text specifically for speech output
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove special characters but keep spaces and basic punctuation
    # Include Unicode ranges for Indian languages (Telugu, Hindi, Tamil)
    cleaned = re.sub(r'[^A-Za-z0-9\u0C00-\u0C7F\u0900-\u097F\u0B80-\u0BFF\s.,!?;:]', '', text)
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned


def init_tts_engine():
    """Initialize the TTS engine with female voice and slower speed"""
    global engine
    if not PYTTSX3_AVAILABLE:
        return None
        
    if engine is None:
        engine = pyttsx3.init()
        
        # Set properties for female voice
        voices = engine.getProperty('voices')
        # Try to find a female voice
        female_voice_found = False
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower() or "catherine" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                female_voice_found = True
                break
        
        # If no female voice found, try to find any voice
        if not female_voice_found and voices:
            engine.setProperty('voice', voices[0].id)
        
        # 🐢 Slow down speed (normal is ~200, slower is ~150)
        engine.setProperty('rate', 150)  # Slower speed for better comprehension
        
        # Set volume
        engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
    
    return engine


def speak_with_pyttsx3(text, language="en"):
    """Speak text using pyttsx3 with slower speed"""
    global engine, is_speaking
    
    if not PYTTSX3_AVAILABLE:
        raise Exception("pyttsx3 not available")
        
    engine = init_tts_engine()
    
    # Clean text for speech
    clean_text_content = clean_text(text)
    
    if not clean_text_content.strip():
        return
    
    def speak():
        global is_speaking
        is_speaking = True
        try:
            engine.say(clean_text_content)
            engine.runAndWait()
        except RuntimeError as e:
            if "run loop already started" in str(e):
                # Try to end the loop and restart
                try:
                    engine.endLoop()
                    engine.say(clean_text_content)
                    engine.runAndWait()
                except:
                    pass
        is_speaking = False
    
    # Run speech in a separate thread to allow interruption
    thread = threading.Thread(target=speak)
    thread.start()
    
    # Wait for speech to complete or be interrupted
    while thread.is_alive() and not stop_flag.is_set():
        time.sleep(0.1)
    
    if stop_flag.is_set():
        try:
            engine.stop()
        except:
            pass
        stop_flag.clear()


def speak_with_gtts(text, language="en"):
    """Speak text using gTTS (Google Text-to-Speech)"""
    global is_speaking
    
    if not GTTS_AVAILABLE:
        raise Exception("gTTS or pygame not available")
        
    # Clean text for speech
    clean_text_content = clean_text(text)
    
    if not clean_text_content.strip():
        return
        
    filename = "zoya_tts.mp3"
    
    try:
        is_speaking = True
        tts = gTTS(text=clean_text_content, lang=language, slow=False, lang_check=False)
        tts.save(filename)
        
        # Initialize and play sound
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Spacebar stop works only while playing
        def monitor_stop():
            while pygame.mixer.music.get_busy():
                if keyboard.is_pressed("space"):
                    pygame.mixer.music.stop()
                    break
        
        # Run stop monitor in background
        threading.Thread(target=monitor_stop, daemon=True).start()
        
        # Wait until speech finishes or is interrupted
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Clean up
        pygame.mixer.quit()
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"[Speech Error]: {e}")
        try:
            pygame.mixer.quit()
        except:
            pass
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        raise
    finally:
        is_speaking = False


def speak_text(text, language="en"):
    """
    Speak the given text using the preferred TTS engine
    
    Args:
        text (str): Text to be spoken
        language (str): Language code for speech
    """
    global is_speaking
    
    if not text:
        return
    
    print(f"Speaking in language: {language}")
    
    # Try pyttsx3 first (with slower speed), fallback to gTTS
    if PYTTSX3_AVAILABLE:
        try:
            speak_with_pyttsx3(text, language)
            return
        except Exception as e:
            print(f"pyttsx3 failed: {e}. Trying gTTS...")
    
    if GTTS_AVAILABLE:
        try:
            speak_with_gtts(text, language)
            return
        except Exception as gTTS_error:
            print(f"gTTS also failed: {gTTS_error}")
    
    print("Text output only:", text)


def stop_speaking():
    """Stop the current speech output"""
    global engine, is_speaking
    stop_flag.set()
    
    if PYTTSX3_AVAILABLE and engine:
        try:
            engine.stop()
        except:
            pass
    
    # Stop gTTS if playing
    if GTTS_AVAILABLE:
        try:
            pygame.mixer.quit()
        except:
            pass
    
    # Only print once when stopping
    print("Speech stopped.")