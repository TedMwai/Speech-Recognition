from datetime import datetime

import azure.cognitiveservices.speech as speechsdk

from constants import NOTION_API_KEY, SPEECH_KEY, SPEECH_REGION, database_id
from notion import NotionClient

client = NotionClient(NOTION_API_KEY, database_id)


# configurations for speech recognition
speech_config = speechsdk.SpeechConfig(
    subscription=SPEECH_KEY, region=SPEECH_REGION)
speech_config.speech_recognition_language = "en-US"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
# configurations for speech synthesis
speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'
audio_config_two = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config)

ACTIVATION_COMMAND = "hello world"

def get_audio():
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    return speech_recognition_result.text


def play_sound(text):
    speech_synthesizer.speak_text_async(text).get()


if __name__ == "__main__":
    command = get_audio()
    print(command)

    if ACTIVATION_COMMAND in command.lower():
        print("Activated")
        play_sound("I'm listening")
        note = get_audio()
        print(note)
        if note:
            play_sound("You said: " + note)
            now = datetime.now().astimezone().isoformat()
            res = client.create_page(note, now, status="Active")
            if res.status_code == 200:
                play_sound("Stored new item")
            else:
                play_sound("Sorry I failed to store the note😔")
