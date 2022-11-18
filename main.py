import os
import speech_recognition as sr
import gtts
from playsound import playsound
import constants
from notion import NotionClient
from datetime import datetime

r = sr.Recognizer()

token = constants.NOTION_API_KEY
database_id = constants.database_id

client = NotionClient(token, database_id)

ACTIVATION_COMMAND = "hello world"

def get_audio():
    with sr.Microphone() as source:
        print("Say something")
        audio = r.listen(source)
    return audio

def audio_to_text(audio):
    text = ""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError:
        print("could not request results from API")
    return text

def play_sound(text):
    try:
        tts = gtts.gTTS(text)
        tempfile = "./temp.mp3"
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)
    except AssertionError:
        print("could not play sound")

if __name__ == "__main__":

    while True:
        a = get_audio()
        command = audio_to_text(a)
        print(command)

        if ACTIVATION_COMMAND in command.lower():
            print("Activated")
            play_sound("I'm listening")

            note = get_audio()
            note = audio_to_text(note)
            print(note)

            if note:
                play_sound("You said: " + note)
                now = datetime.now().astimezone().isoformat()
                res = client.create_page(note, now, status="Active")
                if res.status_code == 200:
                    play_sound("Stored new item")