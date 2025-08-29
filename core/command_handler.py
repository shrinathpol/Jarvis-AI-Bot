# Jarvis/core/command_handler.py
import json
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')

# Create a global chat session object
# This object will store the conversation history
chat_session = model.start_chat(history=[])

def get_gemini_response(user_input):
    """Sends a query and conversation history to Gemini and returns the AI's response."""
    try:
        # Use the chat_session.send_message method
        # This automatically appends the user input and the model's response to the history
        response = chat_session.send_message(user_input)
        
        # Check if the response contains text
        if hasattr(response, 'text'):
            return response.text
        else:
            return "I couldn't generate a text response for that."
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return "I am sorry, I am unable to process that request at the moment."
    
CACHE_FILE = 'data/online_cache.json'

def get_gemini_response(user_input):
    # ... existing try/except block
    try:
        response = chat_session.send_message(user_input)
        if hasattr(response, 'text'):
            # Call the caching function
            save_to_cache(user_input, response.text)
            return response.text
        else:
            return "I couldn't generate a text response for that."
    except Exception as e:
        # ... existing error handling
        return "I am sorry, I am unable to process that request at the moment."

def save_to_cache(query, response):
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        cache = {}
    
    # ...
    
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=4)