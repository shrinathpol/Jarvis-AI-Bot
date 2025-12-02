import cv2
import threading
from ultralytics import YOLO
from core.offline_mode import get_cnc_explanation
from core.speech_engine import speak

class CameraHandler:
    def __init__(self, model_path="models/best.pt"):
        self.model_path = model_path
        self.model = self._load_model()
        self.speak_thread = None

    def _load_model(self):
        try:
            model = YOLO(self.model_path)
            return model
        except Exception as e:
            print(f"Error loading model: {e}. Ensure '{self.model_path}' exists.")
            print("Falling back to a general YOLO model.")
            return YOLO("yolov8n.pt")

    def start_live_assistance(self, stop_event):
        """
        Opens camera, continuously detects objects, and speaks their explanations.
        This function is designed to be run in a separate thread.
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            speak("Error: Could not open camera.")
            print("Error: Could not open camera.")
            return

        last_detected_name = None
        
        print("--- LIVE ASSISTANCE MODE ---")
        print("Say 'stop' or 'exit' to quit.")
        
        while not stop_event.is_set():
            ret, frame = cap.read()
            if not ret: 
                break
            
            results = self.model(frame, verbose=False)
            
            detected_name = None
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    current_name = self.model.names[cls]
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, current_name, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    
                    detected_name = current_name

            cv2.imshow('Live Assistance', frame)

            if detected_name and detected_name != last_detected_name:
                last_detected_name = detected_name
                explanation = get_cnc_explanation(detected_name)
                
                if self.speak_thread is None or not self.speak_thread.is_alive():
                    self.speak_thread = threading.Thread(target=speak, args=(f"I see {detected_name}. {explanation}",))
                    self.speak_thread.start()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("INFO: 'q' pressed, stopping live assistance from keyboard.")
                stop_event.set()
                break

        cap.release()
        cv2.destroyAllWindows()
        
        if self.speak_thread is not None and self.speak_thread.is_alive():
            self.speak_thread.join()
        
        print("--- Live assistance ended. ---")

    def scan_for_explanation(self):
        """
        Opens camera, draws boxes, and waits for user to press 'S' to select an object.
        """
        cap = cv2.VideoCapture(0)
        detected_name = None
        
        print("--- SCAN MODE ---")
        # ... (rest of the function remains the same, just needs to use self.model)
        
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            results = self.model(frame, verbose=False)
            
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    current_name = self.model.names[cls]
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, current_name, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    
                    detected_name = current_name

            cv2.imshow('CNC Scanner - Press S to Select', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                detected_name = None
                break
            if key == ord('s') and detected_name:
                break

        cap.release()
        cv2.destroyAllWindows()
        return detected_name

    def verify_action(self, target_object_name):
        """
        Checks if the user is pointing at the specific target object.
        """
        cap = cv2.VideoCapture(0)
        success = False
        
        print(f"--- VERIFICATION MODE ---")
        # ... (rest of the function remains the same, just needs to use self.model)
        
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            results = self.model(frame, verbose=False)
            target_seen_in_frame = False
            
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    name = self.model.names[cls]
                    
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    if name == target_object_name:
                        color = (0, 255, 0)
                        target_seen_in_frame = True
                        label = f"CORRECT: {name}"
                    else:
                        color = (0, 0, 255)
                        label = f"WRONG: {name}"
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(frame, label, (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            cv2.putText(frame, f"TARGET: {target_object_name}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            cv2.imshow('Safety Verification', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            
            if target_seen_in_frame:
                cv2.waitKey(500)
                success = True
                break

        cap.release()
        cv2.destroyAllWindows()
        return success