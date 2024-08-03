import speech_recognition as sr
from .text_to_speech import speak

def listen():
    """Listen to the user's speech and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=60)
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"\nYou said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that. Please try again.")
        except sr.RequestError as e:
            error_message = f"Sorry, there was an issue with the speech service: {e}"
            speak(error_message)
            print(error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            speak(error_message)
            print(error_message)
    return None
