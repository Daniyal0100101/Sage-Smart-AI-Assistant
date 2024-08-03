
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
