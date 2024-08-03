# Smart Assistant

A comprehensive smart assistant built with Python, integrating speech recognition, text-to-speech, object detection, and various utility functions. This assistant can interact through voice or text modes, perform system tasks, fetch real-time weather, news, and more, making it a versatile tool for daily use.

## Features

- **Speech Recognition**: Converts spoken words into text.
- **Text-to-Speech**: Converts text into spoken words.
- **Object Detection**: Detects objects in real-time using YOLOv5.
- **System Control**: Controls system functions like shutdown, restart, volume control, and more.
- **Real-time Data**: Fetches current weather, news, and Wikipedia summaries.
- **Utility Functions**: Includes features like flipping a coin, rolling a die, telling jokes, and more.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Daniyal0100101/Sage-Smart-AI-Assistant.git
    cd AI Assistant
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
    - Obtain your weather API key and save it in `weather api key.txt`.

## Usage

Run the main script to start the assistant:

```bash
python main.py
