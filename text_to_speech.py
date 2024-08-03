import pyttsx3

def init_tts_engine():
    """Initialize the text-to-speech engine."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 172)
        engine.setProperty('volume', 0.9)
        return engine
    except Exception as e:
        print(f"Error initializing TTS engine: {e}")
        return None

engine = init_tts_engine()

def speak(text):
    """Speak the given text using the TTS engine."""
    if engine:
        engine.say(text)
        engine.runAndWait()
    else:
        print(text)
