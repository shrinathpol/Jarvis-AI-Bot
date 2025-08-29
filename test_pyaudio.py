import pyaudio
import sys

try:
    p = pyaudio.PyAudio()
    print("PyAudio is installed and working correctly.")
    print("Device Information:")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print(f"  Device {i}: {dev['name']}")
    p.terminate()
    print("\nIf you see your microphone in the list, the library can access it.")
except Exception as e:
    print("Error: PyAudio is not installed or configured correctly.")
    print(e)