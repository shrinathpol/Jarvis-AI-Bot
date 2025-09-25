# Jarvis/core/speech_engine.py

import speech_recognition as sr
import pyttsx3
import pyaudio
import re
import threading

# Global flag to control speech interruption
stop_speaking_event = threading.Event()

# Initialize the speech engine
engine = pyttsx3.init()

# Find an Indian English voice
found_voice = None
voices = engine.getProperty('voices')
for voice in voices:
    if "en-in" in voice.languages or "India" in voice.name:
        found_voice = voice
        break

if found_voice:
    engine.setProperty('voice', found_voice.id)
    print(f"Using Indian English Voice: {found_voice.name}")
else:
    print("Indian English voice not found. Using default voice.")

def speak(text):
    """
    Speaks the given text using the initialized engine after cleaning it.
    This function is non-blocking and can be interrupted by setting the stop_speaking_event.
    """
    global stop_speaking_event
    stop_speaking_event.clear()
    
    clean_text = re.sub(r'[^a-zA-Z0-9\s.,?!]', '', text)
    print(f"Jarvis: {clean_text}")

    engine.say(clean_text)
    
    while engine._inLoop and not stop_speaking_event.is_set():
        engine.iterate()
    
    if stop_speaking_event.is_set():
        engine.stop()
        print("Speech interrupted.")

def take_command(lang):
    """Listens for a command from the user and returns the text."""
    r = sr.Recognizer()
    
    # Replace '1' with the device index of your microphone if it's not working
    mic_index = 7
    
    try:
        with sr.Microphone(device_index=mic_index, channels=1) as source:
            print(f"Listening in {lang}...")
            r.pause_threshold = 1.5
            r.adjust_for_ambient_noise(source, duration=2)
            audio = r.listen(source)
    except TypeError:
        print("Warning: Your 'speech_recognition' library is an older version or doesn't support 'channels'.")
        with sr.Microphone(device_index=mic_index) as source:
            print(f"Listening in {lang}...")
            r.pause_threshold = 1.5
            r.adjust_for_ambient_noise(source, duration=2)
            audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language=lang)
        print(f"User said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return "none"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "none"