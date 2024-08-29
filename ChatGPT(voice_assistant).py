import openai
from dotenv import load_dotenv
import os
import speech_recognition as sr
import pyttsx3

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

def speaktext(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

r = sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=1)
                print("I'm listening")
                audio2 = r.listen(source2)
                My_text = r.recognize_google(audio2)
                return My_text
        except sr.RequestError as e:
            print("Could not request results: {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_ChatGPT(messages, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = response.choices[0].message["content"]
        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, something went wrong."

messages = []
while True:
    text = record_text()
    messages.append({'role': 'user', 'content': text})
    response = send_to_ChatGPT(messages)
    speaktext(response)
    print(response)
