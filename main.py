# main.py

import datetime
import requests
import os
import sys
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import threading
import time

# Import core modules
from core.speech_engine import speak, take_command, stop_speaking_event
from core.command_handler import get_gemini_response
from core.offline_mode import handle_offline_command
from core.command_handler import CACHE_FILE as ONLINE_CACHE_PATH
# Import offline inference functions
from offline_model_trainer.src.offline_inference import load_model, preprocess_input, make_prediction

# Global variable to store the chosen language
chosen_language = "en-in"

# Global variable to store the offline model
offline_model = None

def choose_language(language_code):
    """Sets the chosen language for speech recognition and synthesis."""
    global chosen_language
    chosen_language = language_code
    speak(f"Language set to {language_code}")

# Load validation data from JSON file
def load_validation_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['validation_data']

# Load pre-trained sentence transformer model
model_sbert = SentenceTransformer('all-MiniLM-L6-v2')

# Function to calculate similarity between two sentences
def calculate_similarity(query1, query2):
    embedding1 = model_sbert.encode(query1, convert_to_tensor=True)
    embedding2 = model_sbert.encode(query2, convert_to_tensor=True)
    similarity = cosine_similarity([embedding1.cpu().numpy()], [embedding2.cpu().numpy()])[0][0]
    return similarity

# Function to find the best matching response from the validation data
def find_best_match(query, validation_data, similarity_threshold=0.5):
    best_match = None
    max_similarity = 0
    for item in validation_data:
        similarity = calculate_similarity(query, item['input'])
        if similarity > max_similarity and similarity > similarity_threshold:
            max_similarity = similarity
            best_match = item['expected_output']
    return best_match

def is_connected():
    """Check for an active internet connection."""
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def ensure_cache_file_exists():
    """Checks if the cache directory and file exist, creating them if not."""
    cache_dir = os.path.dirname(ONLINE_CACHE_PATH)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    if not os.path.exists(ONLINE_CACHE_PATH):
        with open(ONLINE_CACHE_PATH, 'w', encoding='utf-8') as f:
            f.write('{}')



def wish_me():
    """Greets the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    greeting = ""
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"

    speak(greeting)
    speak("I am Jarvis. How may I assist you?")

def get_offline_response(query, validation_data):
    """Generates a response using the offline validation data."""
    best_match = find_best_match(query, validation_data)
    if best_match:
        return best_match
    else:
        return "I am sorry, I don't have an answer for that offline. I can try online if you want."

def stop_current_speech():
    """Signals the speaking thread to stop."""
    stop_speaking_event.set()
    print("Speech interruption signal sent.")

if __name__ == "__main__":
    ensure_cache_file_exists()

    choose_language("en-us")

    wish_me()

    offline_model_path = os.path.join(os.getcwd(), 'offline_model_trainer', 'models', 'offline_model.pkl')
    try:
        offline_model = load_model(offline_model_path)
        speak("Offline model loaded successfully.")
    except Exception as e:
        print(f"Error loading offline model: {e}")
        speak("Failed to load offline model.")

    validation_data_path = os.path.join(os.getcwd(), 'offline_model_trainer', 'data', 'validation_data.json')
    validation_data = load_validation_data(validation_data_path)

    if not is_connected():
        speak("I am currently in offline mode. Some features may not be available.")
    
    while True:
        query = take_command(lang=chosen_language)
        if query is None:
            continue
        query = query.lower()

        if 'jarvis stop' in query or 'stop' in query:
            stop_current_speech()
            speak("Goodbye!")
            break

        response_text = ""
        if is_connected():
            print("Online mode active.")
            try:
                response_text = get_gemini_response(query)
            except Exception as e:
                print(f"Error from Gemini API: {e}")
                response_text = "I am sorry, there was an issue processing that online. Please try again."
        else:
            print("Offline mode active.")
            response_text = get_offline_response(query, validation_data)
            if "I can try online if you want" in response_text:
                speak("Do you want me to try online?")
                online_attempt = take_command(lang=chosen_language)
                if online_attempt and "yes" in online_attempt.lower():
                    if is_connected():
                        try:
                            response_text = get_gemini_response(query)
                        except Exception as e:
                            print(f"Error from Gemini API: {e}")
                            response_text = "I am sorry, there was an issue processing that online. Please try again."
                    else:
                        response_text = "I am still offline, so I cannot search online."
                else:
                    response_text = "Okay, I will remain offline."
        
        speaking_thread_instance = threading.Thread(target=speak, args=(response_text,))
        speaking_thread_instance.start()
