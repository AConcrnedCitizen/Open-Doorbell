import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 125)
    engine.say(str(text))
    engine.runAndWait()