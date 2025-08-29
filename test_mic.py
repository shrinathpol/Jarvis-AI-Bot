import speech_recognition as sr

# For listing microphones, you can uncomment the line below
print(sr.Microphone.list_microphone_names())

r = sr.Recognizer()

# You can specify the device_index if the default microphone is not correct
# with sr.Microphone(device_index=1) as source:
with sr.Microphone() as source:
    # Adjust for ambient noise to improve recognition accuracy
    print("Adjusting for ambient noise, please wait...")
    r.adjust_for_ambient_noise(source, duration=1)

    print("Say something!")
    try:
        audio = r.listen(source, timeout=10)
        print("Google Speech Recognition thinks you said: " + r.recognize_google(audio))

    except sr.WaitTimeoutError:
        print("No speech was detected within the timeout period.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")