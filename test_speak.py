import pyttsx3

try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Try setting a common Windows voice (Zira or David)
    # You can also try voices[0].id or voices[1].id
    found_test_voice = False
    for voice in voices:
        if "Zira" in voice.name or "David" in voice.name:
            engine.setProperty('voice', voice.id)
            found_test_voice = True
            break

    if not found_test_voice and voices:
        engine.setProperty('voice', voices[0].id) # Fallback to first available voice
        print(f"Using default voice: {voices[0].name}")
    elif found_test_voice:
        print(f"Using test voice: {engine.getProperty('voice')}")
    else:
        print("No voices found on your system.")

    engine.say("Hello, this is a test of the text to speech engine. Can you hear me?")
    print("Attempting to speak...")
    engine.runAndWait()
    print("Speech attempt finished.")
except Exception as e:
    print(f"An error occurred with pyttsx3: {e}")
    print("Please ensure pyttsx3 is correctly installed and your system's text-to-speech is functional.")