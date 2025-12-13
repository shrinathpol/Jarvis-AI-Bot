# Srishti - Voice-Controlled Accessibility Assistant

**Srishti** is an intelligent, voice-controlled accessibility assistant designed to help users operate physical machinery (such as laser cutters or CNC machines) safely and independently.

It combines computer vision (YOLO) for real-time button identification with a hybrid Large Language Model architecture (Google Gemini + Offline Fallback) to answer user queries even when internet connectivity is unstable.

---

## 🏗️ System Architecture

The system follows a strict **Input → Process → Output** flow, featuring an automatic fallback to offline logic if the internet disconnects or if safety policies trigger.

```mermaid
graph TD
    %% Nodes
    User[User's Voice]
    STT[Speech-to-Text (STT) Engine]
    Core[Core Logic (main.py)]
    
    %% Vision Path
    Cam[Camera Feed]
    YOLO[Live Assistance Mode&lt;br/&gt;YOLO Object Detection]
    
    %% Text Path
    NetCheck{Is Internet Connected?}
    Gemini[Online Mode: Gemini API]
    Offline[Offline Logic&lt;br/&gt;ML Classifier/Sentence Sim]
    
    %% Output Path
    Response[Response Text Processor]
    TTS[Text-to-Speech (TTS)&lt;br/&gt;pyttsx3]
    Speaker[Spoken Output]

    %% Connections
    User --&gt; STT
    STT --&gt; Core
    
    %% Logic Splitting
    Core -- "User asks to see" --&gt; YOLO
    Cam --&gt; YOLO
    YOLO --&gt; Response
    
    Core -- "User asks question" --&gt; NetCheck
    
    NetCheck -- Yes --&gt; Gemini
    NetCheck -- No --&gt; Offline
    
    %% Handling Gemini Errors/Safety
    Gemini -- "Success" --&gt; Response
    Gemini -- "Error / Policy Violation" --&gt; Offline
    
    Offline --&gt; Response
    
    %% Final Output
    Response --&gt; TTS
    TTS --&gt; Speaker
```

-----

## 🚀 Features

  * **🎙️ Voice Command Interface:** Hands-free operation using Speech-to-Text and Text-to-Speech.
  * **👁️ Live Visual Assistance:** Uses a webcam and a trained YOLO object detection model to identify control panel buttons and announce them in real-time.
  * **🧠 Hybrid AI Intelligence:**
      * **Online:** Uses Google Gemini API for complex reasoning and general Q\&A.
      * **Offline:** Falls back to a local ML classifier for core command recognition when offline.
  * **🛡️ Safety First:** Automatically routes to offline logic if online models return safety policy violations.

-----

## 📂 Project Structure

```text
Srishti/
├── api_server.py           # Backend server for API handling
├── main.py                 # Entry point of the application
├── config.py               # Main configuration settings
├── requirements.txt        # Project dependencies
├── core/                   # Core application logic
│   ├── camera_handler.py   # YOLO inference & webcam logic
│   ├── command_handler.py  # Routes user intent
│   ├── offline_mode.py     # Local ML fallback logic
│   └── speech_engine.py    # TTS and STT handling
├── data/                   # Knowledge base storage
│   ├── knowledge_base/     # JSON/TXT files for RAG
│   └── online_cache.json   # Caching for offline retrieval
├── models/                 # Place your trained YOLO models here
│   └── best.pt             # (User must provide this)
├── offline_model_trainer/  # Tools to train the offline classifier
│   ├── src/                # Training scripts
│   ├── data/               # Training datasets
│   └── models/             # Output folder for .pkl models
└── test/                   # Testing scripts
```

-----

## ⚙️ Setup & Installation

### 1\. Clone the Repository

```bash
git clone [https://github.com/your-username/Srishti.git](https://github.com/your-username/Srishti.git)
cd Srishti
```

### 2\. Install Dependencies

Ensure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

### 3\. Model Setup

  * **YOLO Model:** Place your trained `best.pt` file inside a `models/` folder in the root directory.
  * **Offline Classifier:** If you do not have the `offline_model.pkl`, navigate to `offline_model_trainer/` and run the training script (refer to documentation inside that folder).

### 4\. API Configuration

Create a `.env` file or update `config.py` with your Google Gemini API Key:

```python
# In config.py
GOOGLE_API_KEY = "your_api_key_here"
```

-----

## 💻 Usage

1.  **Run the application:**

    ```bash
    python main.py
    ```

2.  **Voice Commands:**

      * **"Live assistance"** - Activates the camera and reads out buttons visible on the machine panel.
      * **"Stop" / "Exit"** - Closes the application.
      * **General Questions** - Ask about machine operation (e.g., "How do I turn on the laser?").

-----

<<<<<<< HEAD



graph TD
    %% Nodes
    User[User's Voice]
    STT[Speech-to-Text STT Engine]
    Core[Core Logic main.py]
    
    %% Vision Path
    Cam[Camera Feed]
    YOLO[Live Assistance Mode<br/>YOLO Object Detection]
    
    %% Text Path
    NetCheck{Is Internet Connected?}
    Gemini[Online Mode: Gemini API]
    Offline[Offline Logic<br/>ML Classifier/Sentence Sim]
    
    %% Output Path
    Response[Response Text_Variable]
    TTS[Text-to-Speech TTS<br/>pyttsx3]
    Speaker[Spoken Output]

    %% Connections
    User --> STT
    STT --> Core
    
    %% Logic Splitting
    Core -- "User asks to see" --> YOLO
    Cam --> YOLO
    YOLO --> Response
    
    Core -- "User asks question" --> NetCheck
    
    NetCheck -- Yes --> Gemini
    NetCheck -- No --> Offline
    
    %% Handling Gemini Errors/Safety
    Gemini -- "Success" --> Response
    Gemini -- "Error / Policy Violation" --> Offline
    
    Offline --> Response
    
    %% Final Output
    Response --> TTS
    TTS --> Speaker

## TODO
=======
## ⚠️ Known Issues
>>>>>>> 647fff0 (Update ignore list)

  - **Performance:** The `camera_handler` currently processes every frame, which may cause lag on lower-end devices. Needs optimization (skipping frames).
  - **State Management:** Currently relies on a global dictionary; refactoring to a Class-based state manager is planned.
  - **Configuration:** Config variables are currently scattered. A centralized `config.yaml` or `.env` system is in progress.

## ✅ TODO Roadmap

  - [ ] Refactor `camera_handler.py` for frame skipping/threading.
  - [ ] Centralize configuration into a single `.env` loader.
  - [ ] Replace global dictionary state with a Singleton `StateManager` class.
  - [ ] Clean up project structure (merge `requirements.txt` files).
  - [ ] Add documentation for training the custom YOLO model.

&lt;!-- end list --&gt;
