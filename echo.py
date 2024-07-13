

import speech_recognition as sr
import pyttsx3
import wikipedia
import requests
import datetime
import smtplib
import os
import webbrowser
import json
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL



# Initialize text-to-speech engine
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.pause_threshold = 0.5
        print("Listening...")
        audio = recognizer.listen(source)
        
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language="en-in")
            print(f"Your command: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
            return ""
        except sr.RequestError:
            print("Request error from Google Speech Recognition service")
            return ""

# Function to search Wikipedia
def search_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except wikipedia.exceptions.DisambiguationError:
        return "There are multiple results for this query, please be specific."
    except wikipedia.exceptions.PageError:
        return "No results found."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to get weather information
def get_weather(city):
    api_key = os.getenv('WEATHER_API_KEY', '5d2fa1ad4eb30987cb89ed7dd5c08ab3')
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        main = weather_data["main"]
        temperature = main["temp"]
        weather_desc = weather_data["weather"][0]["description"]
        return f"The temperature in {city} is {temperature}K with {weather_desc}."
    else:
        return "City not found."

# Function to send email
def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('anvatrive2324@gmail.com', os.getenv('EMAIL_PASSWORD', 'Skyanvay@24'))
        server.sendmail('anvatrive2324@gmail.com', to, content)
        server.close()
        return "Email has been sent."
    except Exception as e:
        return f"Sorry, I was not able to send the email. Error: {e}"
    
def add_reminders(task):
    try:
        with open("reminders.json", "r") as file:                 #opening file in read mode
            reminders = json.load(file)                           # reading the file and converting it into a python list
    except FileNotFoundError:
        reminders = []                                            #if file not founf it initialise it as empty list[]

    reminders.append(task)                                        # appending th3e file that is addning a new reminder to the list as task

    with open("reminders.json" , "w") as file :                   # opens the file in write mode 
        json.dump(reminders , file)                               # converts the list back into JSON format 

    return "reminders added"

def list_reminders():
    try : 
        with open ("reminders.json" , "r") as file :
            reminders = json.load(file)
    except FileNotFoundError:
        return "no reminders found"

    return "\n".json(reminders)                                  # joining the list of reminders into a single string with each reminder on a new line                      

# Volume control functions
def set_volume(volume_level):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)    # session allows to control the volume for the session 
        volume.SetMasterVolume(volume_level / 100, None)

def get_volume():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        return volume.GetMasterVolume() * 100

def increase_volume(amount=10):
    current_volume = get_volume()
    new_volume = min(current_volume + amount, 100)
    set_volume(new_volume)

def decrease_volume(amount=10):
    current_volume = get_volume()
    new_volume = max(current_volume - amount, 0)
    set_volume(new_volume)

# Main function to handle commands
def handle_command(command):
    if 'hello' in command:
        speak (" sup bro , what happened ?")
    elif 'bye' in command:
        speak  ("chal thik hai bye!")
        return False
    elif 'search' in command:
        speak  ("What do you want to search for?")
        query = recognize_speech()
        results = search_wikipedia(query)
        speak  (results)
    elif 'weather' in command:
        speak ("Please tell me the city name.")
        city = recognize_speech()
        weather_info = get_weather(city)
        speak  (weather_info)
    elif 'time' in command:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak  (f"The time is {str_time}.")
    elif 'email' in command:
        speak  ("What should I say?")
        content = recognize_speech()
        speak  ("To whom should I send the email?")
        to = recognize_speech()
        email_status = send_email(to, content)
        speak (email_status)
    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        print("Opening YouTube...")
    elif "google" in command:
        query = command.replace("google", "").strip()
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        print(f"Performing Google search for: {query}")
    elif "open" in command:
        website = command.replace("open", "").strip()
        if not website.startswith("http"):
            website = "https://" + website
        webbrowser.open(website)
        print(f"Opening website: {website}") 
    elif "add reminders" in command :
        speak ("what do you want me to remind you sir")
        task = recognize_speech()
        status = add_reminders(task)
        speak(status) 
    elif "list reminders" in command:
        reminders = list_reminders()
        speak(reminders)  
    elif "set volume" in command :
        speak ("what volume level , sir?")
        volume_level = int(recognize_speech())
        set_volume(volume_level)
        speak(f"volume set to {volume_level}%")
    elif "increase volume" in command :
        increase_volume()
        speak("volume increased")
    elif "decrease volume " in  command :
        decrease_volume()
        speak("volume decreased")                
    else:
        speak ("Sorry, I did not get that.")
    return True 

# Main talking function
def talking():
    while True :   
        command  = recognize_speech()
        if command:
            if not handle_command(command):
                break

if __name__ == "__main__" :
    talking()            
            




