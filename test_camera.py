import cv2
import platform

print(f"OpenCV version: {cv2.__version__}")
print(f"Python version: {platform.python_version()}")

# On some systems, you might need to try a different backend
# For example: cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera. 

Troubleshooting tips:
1. Is another program using the camera?
2. Is the camera properly connected?
3. Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` if you have multiple cameras.
4. Try adding `cv2.CAP_DSHOW` like this: `cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)`")
else:
    print("Camera opened successfully. A window should appear. Press 'q' to quit.")
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        
        # Display the resulting frame
        cv2.imshow('Camera Test', frame)
        
        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print("Resources released.")
