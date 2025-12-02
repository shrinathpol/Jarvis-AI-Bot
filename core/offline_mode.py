# core/offline_mode.py

import datetime
import json
from difflib import get_close_matches
from core.speech_engine import speak

# --- CNC KNOWLEDGE BASE ---
# Mapped to the exact class names from your 'data.yaml'
CNC_DATABASE = {
    "Amp_Meter": "This is the Amperage Meter. It monitors the current going to the laser tube.",
    "Display": "This is the Main Display. It shows the file name, speed, and power settings.",
    "Down_button": "This is the Down Button. It moves the laser head towards the front of the bed.",
    "Emergency_Stop": "EMERGENCY STOP! Press this immediately if the machine malfunctions or there is a fire.",
    "Enter_button": "This is the Enter Button. Use it to confirm selections or enter menus.",
    "Esc_button": "This is the Escape Button. Use it to go back or cancel an operation.",
    "File_button": "This is the File Button. Press it to load a design from the controller's memory.",
    "Frame_button": "This is the Frame Button. It traces the bounding box of your design to check alignment.",
    "Left_button": "This is the Left Button. It moves the laser head to the left.",
    "Max-Power_button": "This sets the Maximum Power percentage for cutting.",
    "Min-Power_button": "This sets the Minimum Power percentage for corners.",
    "Origin_button": "This is the Origin Button. It sets the current position as the starting point (0,0).",
    "Power_switch": "This is the Main Power Switch. It turns the machine on.",
    "Pulse_button": "This is the Pulse Button. It fires a short laser burst for alignment testing.",
    "Reset_button": "This is the Reset Button. It clears alarms and resets the controller state.",
    "Right_button": "This is the Right Button. It moves the laser head to the right.",
    "Speed_button": "This is the Speed Button. Use it to adjust travel and cutting speeds.",
    "Start-Pause_button": "This is the Start/Pause Button. It begins the job or pauses it.",
    "Up_button": "This is the Up Button. It moves the laser head towards the back.",
    "Z_U_button": "This button switches control between the Z-axis (height) and U-axis (rotary)."
}

CACHE_FILE = 'data/online_cache.json'

def get_cnc_explanation(detected_object):
    """Returns the explanation for a detected button, with fuzzy matching."""
    # First, try an exact match
    explanation = CNC_DATABASE.get(detected_object)
    if explanation:
        return explanation

    # If no exact match, try to find a close match
    close_matches = get_close_matches(detected_object, CNC_DATABASE.keys(), n=1, cutoff=0.8)
    if close_matches:
        best_match = close_matches[0]
        return f"I see something like a {best_match}. {CNC_DATABASE[best_match]}"
        
    return f"I see {detected_object}, but I don't have a definition for it."

def handle_offline_command(query, context=None):
    """
    Handles user commands when offline.
    
    Args:
        query (str): The user's voice command or a detected object label.
        context (str, optional): The context of the query, e.g., 'live_assistance'. 
                                 Defaults to None for general queries.
    """
    
    # 1. If in live assistance mode, get explanation for the detected object
    if context == 'live_assistance':
        explanation = get_cnc_explanation(query)
        speak(explanation)
        return

    # 2. For general queries, check cache first
    cached_response = check_cache(query)
    if cached_response:
        speak(f"I remember you asked that before. Here is the answer: {cached_response}")
        return
        
    # 3. If not in cache, fall back to keyword-based logic
    lower_query = query.lower()
    
    if 'what is the time' in lower_query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
    
    elif 'hello' in lower_query:
        speak("Hello! I am currently in offline mode. How can I help?")

    elif "status" in lower_query:
        speak("Systems nominal. Camera is ready.")

    else:
        speak("I am currently offline and can only perform a few simple tasks. Please try a different command or ask about a specific button.")

def check_cache(query):
    """Checks the cache for a previously stored response."""
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            return cache.get(query.lower())
    except (FileNotFoundError, json.JSONDecodeError):
        return None
