import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random
import requests

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Speak function
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice command
def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'mimansha' in command:
                command = command.replace('mimansha', '').strip()
                print(command)
                return command
    except Exception as e:
        print("Error:", e)
        return ""
    return ""

# Personalized Greeting
def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    talk(f"{greeting} I am Mimansha. How can I help you today?")

# Weather Update Feature
def get_weather(city):
    api_key = 'your_openweathermap_api_key'  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            talk(f"The weather in {city} is currently {weather} with a temperature of {temp}°C.")
        else:
            talk("I couldn't fetch the weather information. Please try again.")
    except Exception as e:
        talk("An error occurred while fetching the weather.")
        print("Weather Error:", e)

# Fun Feature: Math Quiz
def math_quiz():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    talk(f"What is {num1} plus {num2}?")
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            answer = listener.recognize_google(voice)
            if int(answer) == (num1 + num2):
                talk("Correct! Well done.")
            else:
                talk(f"Sorry, the correct answer is {num1 + num2}.")
    except Exception as e:
        talk("I couldn't understand your answer. Please try again.")
        print("Math Quiz Error:", e)

# Main function to run the assistant
def run_mimansha():
    greet_user()
    while True:
        command = take_command()
        if not command:
            continue
        if 'play' in command:
            song = command.replace('play', '').strip()
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%H:%M %p')
            talk(f"Current time is {time}")
        elif 'who is' in command:
            person = command.replace('who is', '').strip()
            info = wikipedia.summary(person, sentences=2)
            talk(info)
        elif 'weather in' in command:
            city = command.replace('weather in', '').strip()
            get_weather(city)
        elif 'date' in command:
            talk("Sorry, I have a headache.")
        elif 'joke' in command:
            joke = pyjokes.get_joke()
            talk(joke)
        elif 'math quiz' in command:
            math_quiz()
        elif 'stop' in command or 'exit' in command:
            talk("Goodbye! Have a great day.")
            break
        else:
            talk("Sorry, I didn't understand. Can you please repeat?")

# Start the assistant
run_mimansha()
