"""
Utility functions for Zoya AI Assistant
"""

import re
import threading


# Global stop flag for interrupting speech
stop_flag = threading.Event()


def clean_text(text):
    """
    Clean text by removing special characters and formatting
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove special characters but keep spaces and basic punctuation
    cleaned = re.sub(r'[^\w\s.,!?;:]', '', text)
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned


def reset_stop_flag():
    """Reset the stop flag"""
    stop_flag.clear()


def is_stop_requested():
    """Check if stop has been requested"""
    return stop_flag.is_set()