import os
import requests
import feedparser
import wikipedia
import schedule
import datetime, time
import random
import spacy
import pyjokes
import pyautogui
import psutil
import ollama
import re
import webbrowser
from googlesearch import search
from .text_to_speech import speak
from .speech_recognition import listen
from .system_control import control_system
from .object_detection import model
import cv2

nlp = spacy.load("en_core_web_sm")

def greet():
    """Generate a greeting based on the current time."""
    hr = int(time.strftime('%H'))
    if 4 < hr < 12:
        return "Good morning"
    elif 12 <= hr < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def handle_query(query: str, online: bool):
    """Handle the user's query and provide the appropriate response."""
    if not query:
        return

    query = query.lower()
    response = ''
    
    doc = nlp(query)
    entities = {ent.label_: ent.text for ent in doc.ents}
    
    try:
        if "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"{random.choice(['The time now is', 'The current time is', 'It is'])} {current_time}."

        elif "date" in query:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            response = f"{random.choice(['Today is', 'The day is', 'Today date is'])} {current_date}."

        elif "set a task" in query:
            schedule_time = entities.get("TIME", query.split("for", 1)[-1].strip())
            response = add_task(schedule_time) if schedule_time else "Please specify a valid schedule time."

        elif "delete a task" in query:
            task_name = entities.get("TASK", query.split("for", 1)[-1].strip())
            response = remove_task(task_name) if task_name else "Please specify a valid task name."

        elif "show all tasks" in query:
            response = show_tasks()

        elif "flip a coin" in query:
            response = f"The coin flip result is {random.choice(['Heads', 'Tails'])}."

        elif "roll a die" in query:
            response = f"The dice roll result is {random.randint(1, 6)}."

        elif "joke" in query:
            response = tell_joke()

        elif "type" in query or "write" in query:
            text = entities.get("TEXT", query.split("write", 1)[-1].strip() if "write" in query else query.split("type", 1)[-1].strip())
            if text:
                pyautogui.typewrite(text)
                response = "Typing text..."
            else:
                response = "Please specify the text to be written."

        elif "press" in query or "hit" in query:
            button_name = entities.get("BUTTON", query.split("press", 1)[-1].strip() if "press" in query else query.split("hit", 1)[-1].strip())
            if button_name:
                pyautogui.press(button_name)
                response = f"Pressing {button_name}"
            else:
                response = "Please specify the button to be pressed."

        elif "open" in query:
            app_name = entities.get("APPLICATION", query.split("open", 1)[-1].strip())
            if app_name:
                os.system('start ' + app_name)
                response = f"Opening {app_name}."
            else:
                response = "Please specify an application to open."

        elif "close" in query:
            app_name = entities.get("APPLICATION", query.split("close", 1)[-1].strip())
            if app_name:
                os.system(f"taskkill /F /IM {app_name}.exe")
                response = f"Closing {app_name}."
            else:
                response = "Please specify an application to close."

        elif "screenshot" in query:
            response = control_system("screenshot")

        elif "shutdown" in query:
            speak("Shutting down the system.")
            control_system("shutdown")
            return

        elif "restart" in query:
            speak("Restarting the system.")
            control_system("restart")
            return

        elif "log off" in query:
            speak("Logging off the system.")
            control_system("log off")
            return

        elif "volume up" in query:
            speak("Increasing volume.")
            control_system("volume up")

        elif "volume down" in query:
            speak("Decreasing volume.")
            control_system("volume down")

        elif "mute" in query:
            speak("Muting volume.")
            control_system("mute")

        elif "unmute" in query:
            speak("Unmuting volume.")
            control_system("unmute")

        elif "system info" in query:
            response = get_system_info()

        elif "set brightness" in query:
            try:
                level = int(entities.get("BRIGHTNESS", query.split("set brightness to", 1)[-1].strip()))
                response = control_system(f"brightness {level}")
            except ValueError:
                response = "Please specify a valid brightness level between 0 and 100."

        elif "object detection" in query or "detect object" in query:
            if model is None:
                response = "Object detection model is not available."
            else:
                speak("Activating object detection.")
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    response = "Failed to open camera."
                else:
                    detected_objects = []
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            speak("Failed to capture video frame.")
                            break

                        results = model(frame)
                        for *box, conf, cls in results.xyxy[0]:
                            cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                            cv2.putText(frame, f"{model.names[int(cls)]} {conf:.2f}", (int(box[0]), int(box[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                            detected_objects.append(model.names[int(cls)])
                        
                        cv2.imshow('Object Detection', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            speak("Do you have any questions about the objects?")
                            reply = listen()
                            if "yes" in reply:
                                question = f"Answer the query: {reply.split('yes')[-1].strip()}\nHere are the objects: {', '.join(detected_objects)}"
                                response = get_response(question)
                            else:
                                response = f"I detected objects: {', '.join(detected_objects)}"
                            break
                    cap.release()
                    cv2.destroyAllWindows()

        elif "hi" in query or "hello" in query:
            response = random.choice(["Hi", "Hello", "Hello! How can I help you today?", "How may I help you today?"])

        elif "what is your name" in query or "what's your name" in query:
            response = random.choice(["My name is Sage.", "I'm Sage", "My name is Sage! What's your name?"])
        
        elif any(word in query for word in word_to_operator.keys() | {'+', '-', '*', '/'}):
            try:
                for word, operator in word_to_operator.items():
                    query = query.replace(word, operator)
                
                expression = ''.join(re.findall(r'[0-9\+\-\*/\(\) ]+', query))
                if expression:
                    result = secure_eval(expression)
                    response = f"The {expression} equals {result}"
                else:
                    response = "I couldn't find a valid mathematical expression in your input."
            except Exception as e:
                response = f"An error occurred while performing the calculation: {e}"
        
        elif "save a note" in query or "take note" in query:
            note = entities.get("NOTE", query.split("remember", 1)[-1].strip() if "remember" in query else query.split("take note", 1)[-1].strip())
            if note:
                save_to_file(note)
                response = "I've saved your note."
            else:
                response = "Please provide a note to be remembered."

        elif "tell note" in query or "what you remember" in query:
            response = load_from_file()

        elif 'weather' in query and online:
            city_name = get_current_city()
            if city_name:
                response = get_weather(city_name) if city_name else "Please specify a city for the weather forecast."

        elif "news" in query and online:
            response = get_news()

        elif "search" in query:
            search_query = entities.get("SEARCH_QUERY", query.split("search ", 1)[-1].strip())
            if search_query:
                try:
                    results = list(search(search_query, num_results=2))
                    response = "Opening the top search result."
                    webbrowser.open(results[0])
                except Exception as e:
                    response = f"Error performing Google search: {e}"
            else:
                response = "Please specify a search query."

        elif 'wikipedia' in query and online:
            speak("Please tell me the topic.")
            wiki_topic = listen()
            if wiki_topic:
                response = get_wikipedia_summary(wiki_topic)
            else:
                response = "Please specify a topic for the Wikipedia summary."

        else:
            response = get_response(query)

    except Exception as e:
        response = f"An error occurred: {e}"

    if response:
        print("AI: " + response)
        speak(response.strip())

def get_news():
    """Fetch real-time news from an RSS feed."""
    try:
        rss_url = "https://news.google.com/rss?hl=en-PK&gl=PK&ceid=PK:en"
        feed = feedparser.parse(rss_url)
        if feed.entries:
            first_article_title = feed.entries[0].title
            return f"Here's the latest news: {first_article_title}"
        return "No news articles found."
    except Exception as e:
        return f"Error fetching news: {e}"

def get_weather(city):
    """Fetch real-time weather data for a specified city."""
    try:
        api_key_path = Explain_API_Key_Path_Add_Your_own"
        if not os.path.isfile(api_key_path):
            return "The file containing the API key could not be found."

        with open(api_key_path, "r") as file:
            api_key = file.read().strip()

        if not api_key:
            return "The API key is missing from the file."

        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(base_url)
        data = response.json()

        if data.get("cod") != 200:
            return f"Could not find weather information for {city}. Please check the city name or try again later."

        main = data["main"]
        weather_description = data["weather"][0]["description"]
        temperature = main["temp"]
        humidity = main["humidity"]
        pressure = main["pressure"]
        wind_speed = data["wind"]["speed"]

        return (f"Here's the weather update for {city}:\n"
                f"- Current temperature: {temperature:.1f}°C\n"
                f"- Weather condition: {weather_description.capitalize()}\n"
                f"- Humidity level: {humidity}%\n"
                f"- Atmospheric pressure: {pressure} hPa\n"
                f"- Wind speed: {wind_speed:.1f} m/s")

    except Exception as e:
        return f"An error occurred while fetching the weather data: {e}"

def get_wikipedia_summary(topic):
    """Fetch a summary from Wikipedia for the given topic."""
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found for '{topic}', please be more specific."
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{topic}'."
    except Exception as e:
        return f"An error occurred while fetching the Wikipedia summary: {e}"

def get_system_info():
    """Get system information such as CPU usage, memory usage, and battery status."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    battery = psutil.sensors_battery()
    battery_status = battery.percent if battery else "Unknown"
    return f"CPU usage is at {cpu_usage}%. Memory usage is at {memory_usage}%. Battery is at {battery_status}%."

def tell_joke():
    """Tell a random joke."""
    try:
        joke = pyjokes.get_joke(language='en', category='all')
        return joke
    except Exception as e:
        return f"Error fetching joke: {e}"

def get_current_city():
    """Get the current city based on the IP address."""
    # Get IP address to determine location
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json()['ip']

    # Use an IP geolocation API to get location based on IP address
    response = requests.get(f'https://ipinfo.io/{ip_address}/json')
    location = response.json()

    city = location.get('city', 'City not found')
    return city

def add_task(schedule_time):
    """Add a scheduled task at the specified time."""
    try:
        schedule.every().day.at(schedule_time).do()
        return f"Task scheduled for {schedule_time}."
    except Exception as e:
        return f"Error scheduling task: {e}"

def remove_task(task_name):
    """Remove a scheduled task by name."""
    try:
        for job in schedule.get_jobs():
            if job.job_func.func.__name__ == 'job' and job.tags[0] == task_name:
                schedule.cancel_job(job)
                return f"Task '{task_name}' removed successfully."
        return f"No task found with name '{task_name}'."
    except Exception as e:
        return f"Error removing task: {e}"

def show_tasks():
    """Show all scheduled tasks."""
    tasks = schedule.get_jobs()
    if not tasks:
        return "No scheduled tasks found."
    task_list = "\n".join([f"{job.job_func.func.__name__} at {job.next_run}" for job in tasks])
    return f"Scheduled tasks:\n{task_list}"

def save_to_file(note):
    """Save a note to a file."""
    try:
        with open("notes.txt", "a") as file:
            file.write(f"{datetime.datetime.now()}: {note}\n")
        return "Note saved successfully."
    except Exception as e:
        return f"Error saving note: {str(e)}"

def load_from_file():
    """Load notes from a file."""
    try:
        notes = []
        with open("notes.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                notes.append(line.strip())
        return notes
    except Exception as e:
        return f"Error loading notes: {str(e)}"

def secure_eval(expression):
    """Evaluate a mathematical expression securely."""
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except Exception as e:
        return f"Error evaluating the expression: {e}"

def get_response(request):
    """Get a response from the LLVM model."""
    print('Thinking...\n')
    try:
        response = ollama.generate(
            model="Replace-with-actual-model-name",
            prompt=request
        )
        return response['response']
    except Exception as e:
        return f"Error generating LLM response: {e}"

word_to_operator = {
    '+': '+',
    '-': '-',
    'x': '*',
    '÷': '/',
    'plus': '+',
    'minus': '-',
    'multiply': '*',
    'multiply by': '*',
    'divided by': '/',
    'divide': '/',
    'power': '**'
}
