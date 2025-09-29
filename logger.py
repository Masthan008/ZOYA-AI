"""
Handles logging of Zoya AI Assistant interactions to JSON file
"""

import json
import os
from datetime import datetime

LOG_FILE = "zoya_logs.json"


def log_interaction(user_query, ai_reply, mode="text", search_result=None):
    """
    Save interaction into JSON log file.
    
    Args:
        user_query (str): The user's query
        ai_reply (str): The AI's response
        mode (str): The mode used (text or voice)
        search_result (str): Search results if used, None otherwise
    """
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": mode,
        "user_query": user_query,
        "ai_reply": ai_reply,
        "search_result": search_result
    }

    # Load existing logs
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(log_entry)

    # Save updated log
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

    print(f"🗂️ Logged conversation: {log_entry['timestamp']}")


def get_logs():
    """
    Retrieve all logged interactions
    
    Returns:
        list: List of log entries
    """
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def clear_logs():
    """Clear all logged interactions"""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print("🗑️ Logs cleared")