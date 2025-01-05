import os
import json
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
from time import sleep

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def load_settings():
    """Load user settings from settings.json."""
    with open("config/settings.json", "r") as file:
        return json.load(file)

def listen_to_user():
    """Listens to the user's voice input and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return None
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return None

def get_time():
    """Returns the current time in HH:MM:SS format."""
    return datetime.datetime.now().strftime("%H:%M:%S")

def open_website(url):
    """Opens a website in the browser."""
    webbrowser.open(url)
    speak(f"Opening {url}")

def play_music(music_path):
    """Plays music from the specified folder."""
    if os.path.exists(music_path):
        songs = os.listdir(music_path)
        if songs:
            os.startfile(os.path.join(music_path, songs[0]))
            speak("Playing music.")
        else:
            speak("No music files found.")
    else:
        speak("Music folder not found.")

def get_weather(city):
    """Fetches the weather information for the given city."""
    API_KEY = "0ab0a939aa5061f8670c965e813bdc43"  # Use OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] == 200:
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        description = weather["description"]
        return f"The temperature in {city} is {temperature}°C with {description}."
    else:
        return "Sorry, I couldn't fetch the weather."

def perform_task(command, settings):
    """Performs tasks based on user commands."""
    if "time" in command:
        speak(f"The current time is {get_time()}.")
    elif "weather" in command:
        city = settings["default_city"]
        weather_info = get_weather(city)
        speak(weather_info)
    elif "open youtube" in command:
        open_website("https://www.youtube.com")
    elif "open google" in command:
        open_website("https://www.google.com")
    elif "play music" in command:
        music_folder = settings["music_folder"]
        play_music(music_folder)
    elif "exit" in command:
        speak("Goodbye!")
        exit(0)
    else:
        speak("Sorry, I don't understand that command.")

def main():
    settings = load_settings()
    speak("Welcome to your personal assistant.")
    while True:
        command = listen_to_user()
        if command:
            perform_task(command, settings)

if __name__ == "__main__":
    main()
