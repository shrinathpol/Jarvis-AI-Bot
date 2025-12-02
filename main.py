# main.py - Consolidated application logic

import speech_recognition as sr
from core.camera_handler import CameraHandler
from core.offline_mode import handle_offline_command
from core.speech_engine import speak
from core import online_model_handler
from core.config import GOOGLE_API_KEY
import threading
import socket
import time
import vlc
import win32gui
import os
import sys

# --- State Management ---
command_in_progress_flag = threading.Event()
exit_event = threading.Event()
live_assistance_thread = None
live_assistance_stop_event = threading.Event()

def is_internet_available():
    """Checks for a live internet connection."""
    try:
        # Connect to a known reliable server (Google's DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def listen_for_commands():
    """Main loop to listen for and handle voice commands."""
    global live_assistance_thread
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening for commands...")

    while not exit_event.is_set():
        if command_in_progress_flag.is_set():
            time.sleep(0.1)
            continue

        query = ""
        audio = None
        with mic as source:
            try:
                speak("listening for commands")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                speak("no speech detected")
                continue
        
        if audio:
            try:
                # Use Google's speech recognition
                query = r.recognize_google(audio,language="en-IN").lower()
                if query:
                    print(f"User said: {query}")
            except sr.UnknownValueError:
                # API was unable to understand the audio
                continue
            except sr.RequestError as e:
                # API was unreachable or returned an error
                print(f"Google API error: {e}")
                if is_internet_available():
                     speak("There seems to be an issue with the online service. Switching to offline mode.")
                continue
        
        if not query:
            continue

        # Check if live assistance is running and handle stop commands
        if live_assistance_thread and live_assistance_thread.is_alive():
            if "stop" in query or "exit" in query:
                print("Stopping live assistance.")
                speak("Stopping live assistance.")
                live_assistance_stop_event.set()
                live_assistance_thread.join()
                live_assistance_thread = None
            else:
                speak("Live assistance is currently active. Say 'stop' to end it.")
            continue
        
        handle_command(query)

def handle_command(query):
    """Dispatches a command to be handled in a new thread."""
    global live_assistance_thread

    if "live" in query:
        speak("Starting live assistance.")
        live_assistance_stop_event.clear()
        handler = CameraHandler()
        # Run live assistance in a separate thread to keep the main loop responsive
        live_assistance_thread = threading.Thread(
            target=handler.start_live_assistance, 
            args=(live_assistance_stop_event,)
        )
        live_assistance_thread.start()
        return
    if "start" in query:
        
        
        speak("So to setup the machine , first press the power button , then wait for the system to boot up completely , after that press the start button to begin operation.")
        speak("Here is a tutorial to guide you")
        hwnd = win32gui.GetForegroundWindow()
        video = "data/video_clips/clip2.mp4"
        player = vlc.MediaPlayer(video)
        player.set_hwnd(hwnd)
        player.play()
        time.sleep(1)

        # Keep script alive while video plays
        while True:
            state = player.get_state()
            if state in [vlc.State.Ended, vlc.State.Error]:
                player.stop()
                player.release()
                break
            time.sleep(0.5)
        return 
    # Handle other commands in a separate thread
    command_thread = threading.Thread(target=run_command, args=(query,))
    command_thread.start()

def run_command(query):
    """
    Handles a non-live-assistance command by routing to online or offline mode.
    """
    command_in_progress_flag.set()
    try:
        if "exit" in query:
            speak("Goodbye!")
            exit_event.set()
        else:
            if is_internet_available():
                # Use the online model for a response
                response = online_model_handler.get_gemini_response(query)
                speak(response)
            else:
                # Fallback to offline mode
                handle_offline_command(query)
    finally:
        # Release the flag so other commands can be processed
        command_in_progress_flag.clear()

def main():
    """
    Main entry point for the voice-controlled accessibility assistant.
    """
    print("Srishti - Voice-Controlled Accessibility Assistant")
    print("Initializing...")
    
    # Start listening for commands
    listen_for_commands()

    print("Shutting down.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutdown requested by user.")
        # Set the event to signal all threads to exit gracefully
        exit_event.set()
