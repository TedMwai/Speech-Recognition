import os
import time
import wave
from datetime import datetime
from io import BytesIO

import azure.cognitiveservices.speech as speechsdk
import numpy as np
import pdfkit
import scipy.io.wavfile as wav
import sounddevice as sd
from PIL import Image

import streamlit as st
from constants import NOTION_API_KEY, SPEECH_KEY, SPEECH_REGION, database_id
from notion import NotionClient

# create notion client
client = NotionClient(NOTION_API_KEY, database_id)

# function to recognize speech from file
def transcribe_audio(file):
    with wave.open(file, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=file)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    transcribed_text = ""
    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            nonlocal transcribed_text
            transcribed_text += evt.result.text

    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.start_continuous_recognition()
    time.sleep(duration//2)
    speech_recognizer.stop_continuous_recognition()
    return transcribed_text

def from_mic():
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    return result.text

def download_text(text):
    # Create a PDF with the transcribed text
    filename = "notes"
    pdf = f"{filename}.pdf"
    pdfkit.from_string(text, pdf)
    return pdf

def send_to_notion(text):
    now = datetime.now().astimezone().isoformat()
    res = client.create_page(text, now, status="Active")
    if res.status_code == 200:
        st.write("Saved note to Notion")
    else:
        st.write("Failed to save note to Notion😢")

def main():
    st.set_page_config(page_title="Audio Transcriber", page_icon=":microphone:", layout="wide")

    st.title("Audio Transcription")

    col1, col2 = st.columns(2)

    with col1:
        # Upload audio file
        audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg", "flac", "m4a"])
        if audio_file is not None:
            st.write(audio_file)
            st.audio(audio_file)

    with col2:
        # Transcribe audio file and show the text
        if audio_file is not None:
            transcribed_text = transcribe_audio(audio_file.name)
            st.success("Audio transcribed successfully")
            st.write("Transcribed Text:")
            st.text_area(label="", value=transcribed_text, height=200)

            # Download button
            if st.button("Download as PDF"):
                pdf_file = download_text(transcribed_text)
                st.success("PDF downloaded successfully")

                # Get the binary content of the PDF file
                with open(pdf_file, "rb") as f:
                    pdf_bytes = f.read()

                # Create a memory stream of the PDF file
                pdf_stream = BytesIO(pdf_bytes)
                st.write("Downloaded PDF:")
                st.markdown("<a href='{}' download>Download PDF</a>".format(pdf_file), unsafe_allow_html=True)
                st.write("Or Download it by clicking on the link above")
            #upload transcribed text to notion
            if st.button("Save to Notion"):
                now = datetime.now().astimezone().isoformat()
                res = client.create_page(transcribed_text, now, status="Active")
                if res.status_code == 200:
                    st.write("Saved note to Notion🎊🎊")
                else:
                    st.write("Failed to save note to Notion😢")


if __name__ == "__main__":
    main()
