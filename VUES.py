from gtts import gTTS
import speech_recognition as sr
import os
import re
from subprocess import call
import webbrowser
import smtplib
import requests
import pyaudio
#import pyttsx
import speech_recognition
import pyttsx3
import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")
from weather import Weather
from pynput.keyboard import Key, Controller
keyboard = Controller()

#name=""




def myCommand():
    "listens for commands"
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Ready...")
        speak.Speak("ready")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=.5)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print("You said: " + command + "\n")
        speak.Speak("You said: " + command + "\n")

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print("Your last command couldn\"t be heard")
        command = myCommand()

    return command


def assistant(command):
    "if statements for executing commands"

    if "login portal" in command:
        reg_ex = re.search("open portal (.*)", command)
        url = "https://portal.aiub.edu/"
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + "r/" + subreddit
        webbrowser.open(url)
        print("Done!")
        
        keyboard.press(Key.cmd)
        keyboard.press(Key.ctrl)
        keyboard.press('o')
        keyboard.release('o')
        keyboard.release(Key.ctrl)
        keyboard.release(Key.cmd)
        #print("Done!")

        speak.Speak("please provide your id and password")



    elif "open calculator" in command:
        call(["calc.exe"])
        print("Done!")
        


    elif "open website" in command:
        reg_ex = re.search("open website (.+)", command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = "https://www." + domain
            webbrowser.open(url)
            print("Done!")
        else:
            pass

    elif "what's up" in command:
        speak.Speak("Just doing my thing")


    elif "joke" in command:
        res = requests.get(
                "https://icanhazdadjoke.com/",
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            speak.Speak(str(res.json()["joke"]))
        else:
            speak.Speak("oops!I ran out of jokes")

    elif "current weather in" in command:
        reg_ex = re.search("current weather in (.*)", command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            condition = location.condition()
            speak.Speak("The Current weather in %s is %s The temperature is %.1f degree" % (city, condition.text(), (int(condition.temp())-32)/1.8))

    elif "weather forecast in" in command:
        reg_ex = re.search("weather forecast in (.*)", command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            forecasts = location.forecast()
            for i in range(0,3):
                speak.Speak("On %s will it %s. The maximum temperture will be %.1f degree."
                         "The lowest temperature will be %.1f degrees." % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))


    elif "email" in command:
        speak.Speak("Who is the recipient?")
        recipient = myCommand()

        if "John" in recipient:
            speak.Speak("What should I say?")
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP("smtp.gmail.com", 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login("username", "password")

            #send message
            mail.sendmail("John Fisher", "JARVIS2.0@protonmail.com", content)

            #end mail connection
            mail.close()
            
            speak.Speak("Email sent.")

        else:
            speak.Speak("I don't know what you mean!")
            


#speak.Speak("I am ready for your command")

#loop to continue executing multiple commands
while True:
    assistant(myCommand())