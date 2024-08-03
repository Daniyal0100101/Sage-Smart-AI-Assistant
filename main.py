import random
from modules.text_to_speech import speak
from modules.speech_recognition import listen, sr
from modules.system_control import is_connected
from modules.utils import greet, handle_query

def main():
    # Check if the system is connected to the internet
    online = is_connected()
    greeting = f"{greet()} {random.choice([f'I am {"connected to the internet" if online else "Not connected to the internet"}; How can I assist you today?', 'How can I help you today?', 'How may I help you today?'])}"
    
    separator = "─" * 60
    print(f"\n{separator}\n{greeting}\n{separator}\n")
    speak(greeting)
    
    # Default mode is text if offline, voice if online
    mode = 'text' if not online else 'voice'
    
    while True:
        try:
            # Get query from user based on mode
            if mode == 'voice':
                query = listen()
            else:
                query = input("\nYou: ")
            
            if query:
                query_lower = query.lower()
                
                # Switch between voice and text mode
                if "switch to" in query_lower:
                    mode = query_lower.split("switch to ")[-1].strip()
                    if mode == "voice mode":
                        if online:
                            print("Switching to voice mode.\n")
                            speak("Switching to voice mode.")
                            mode = 'voice'
                        else:
                            speak("Switching to text mode; Voice mode is not available offline.")
                            mode = 'text'
                    
                    elif mode == "text mode":
                        print("Switching to text mode.\n")
                        speak("Switching to text mode.")
                        mode = 'text'
                
                # Exit the program
                if any(keyword in query_lower for keyword in ['exit', 'break', 'quit', 'stop', 'bye', 'goodbye']):
                    farewell = "Goodbye! Have a great day!"
                    print(farewell)
                    speak(farewell)
                    break
                
                # Handle user query
                handle_query(query, online)
        
        except KeyboardInterrupt:
            print("\nInterrupted by user.\nExiting...")
            break
        
        except sr.UnknownValueError:
            print("Sorry, I did not understand that. Please try again.")
            speak("Sorry, I did not understand that. Please try again.")
        
        except sr.RequestError as e:
            error_message = f"Could not request results from Google Speech Recognition service; {e}"
            print(error_message)
            speak(error_message.strip())
        
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)
            speak(error_message.strip())

if __name__ == "__main__":
    main()
