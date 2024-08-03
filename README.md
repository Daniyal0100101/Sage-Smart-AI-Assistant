
# Smart AI Assistant

A comprehensive smart assistant built with Python, integrating speech recognition, text-to-speech, object detection, and various utility functions. This assistant can interact through voice or text modes, perform system tasks, fetch real-time weather, news, and more, making it a versatile tool for daily use.

## Features

- **Speech Recognition**: Converts spoken words into text.
- **Text-to-Speech**: Converts text into spoken words.
- **Object Detection**: Detects objects in real-time using YOLOv5.
- **System Control**: Controls system functions like shutdown, restart, volume control, and more.
- **Real-time Data**: Fetches current weather, news, and Wikipedia summaries.
- **Utility Functions**: Includes features like flipping a coin, rolling a die, telling jokes, and more.

## Project Structure
```plaintext
smart_assistant/
|-- main.py
|-- modules/
    |-- __init__.py
    |-- object_detection.py
    |-- speech_recognition.py
    |-- system_control.py
    |-- text_to_speech.py
    |-- utils.py
|-- requirements.txt
```

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Daniyal0100101/Sage-Smart-AI-Assistant.git
    cd Sage-Smart-AI-Assistant
    ```

2. **Set Up a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Download Additional Models and Files**
    - Ensure you have the YOLOv5 model (`yolov5s.pt`) and place it in the appropriate directory.
    - Obtain your weather API key and save it in `modules/weather_api_key.txt`.

## Usage

Run the main script to start the assistant:

```bash
python main.py
```

## Configuration

- **Weather API**: Place your weather API key in a file named `weather_api_key.txt` in the `modules` directory.
- **YOLOv5 Model**: Download the `yolov5s.pt` model and place it in the appropriate directory as specified in `object_detection.py`.

## Enhancements

- **Logging**: Logs important events and errors for better debugging.
- **Dockerization**: A Dockerfile for containerized deployment.
- **Unit Tests**: Implement unit tests for all modules.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Contact

For any inquiries, please contact:

- [Daniyal](mailto:your.email@dasif1477@gmail.com)
- [GitHub Profile](https://github.com/Daniyal0100101)
```

### This is the main file

#### `main.py`
```python
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
```
