import os
import speech_recognition as sr
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
from vertexai.language_models import CodeChatModel
from google.cloud import texttospeech
import pyaudio
import argparse
from backchannel import BackchannelDetector
from gesturehandler import GestureHandler
import random
import threading
import wave
import time
import signal
import sys
import demoji

PROJECT_ID = "duck-414417"
GOOGLE_CLOUD_CREDENTIALS = "./creds.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CLOUD_CREDENTIALS

AI_MODEL = "codechat-bison@002"
LOCATION = "us-central1"
VOICE_MODEL = "en-US-Journey-F"
FRAME_SIZE = 4096
AUDIO_RATE = 44100

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-t', '--text', action='store_true')
parser.add_argument('-i', '--intro', action='store_true')

args = parser.parse_args()

def speech_to_text():
    print("Recognizing speech...")
    rec = sr.Recognizer()
    rec.energy_threshold = 300
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=0.5)
        audio = rec.listen(source)
        try:
            text = rec.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_CREDENTIALS)
        except:
            print("No audio recognized!")
            return ""
        return text
    return ""

def llm_respond(model, input_text):
    print("Using LLM to generate response...")
    if args.verbose: print("Input: " + input_text)
    text_response = []
    start = time.time()
    responses = chat.send_message_streaming(input_text)

    part = ""
    sentence_queue = []
    for response in responses:
        part += response.text

        while part.find("!") != -1 or part.find(".") != -1 or part.find("?") != -1:
            div = 0

            first_ex = part.find("!")
            if(first_ex == -1): first_ex = len(part)
            first_pe = part.find(".")
            if(first_pe == -1): first_pe = len(part)
            first_qu = part.find("?")
            if(first_qu == -1): first_qu = len(part)

            div = min(first_ex, first_pe, first_qu)

            sentence = part[0:div + 1]
            sentence_queue.append(sentence)
            part = part[div + 1::]

        while len(sentence_queue) != 0: 
            yield sentence_queue.pop(0)

def play_audio(output, wav):
    data = wav.readframes(FRAME_SIZE)
    while data:
        output.write(data)
        data = wav.readframes(FRAME_SIZE)
    wav.close()

def text_to_speech(client, output, input_text):
    print("Speaking...")
    input_text = demoji.replace(input_text, "")
    if args.verbose: print("Output: " + input_text)
    voice = texttospeech.VoiceSelectionParams(
        name=VOICE_MODEL,
        language_code="en-US"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100
    )
    synthesis_input = texttospeech.SynthesisInput(text=input_text)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open("output.wav", "wb") as out:
        out.write(response.audio_content)
        out.close()
    wf = wave.open("output.wav", 'rb')
    speak_thread = threading.Thread(target=play_audio, args = (output, wf,))
    speak_thread.daemon = True
    speak_thread.start()
    return wf.getnframes() / float(wf.getframerate())

with open('prompt.txt', 'r') as file:
    prompt = file.read()

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = CodeChatModel.from_pretrained(AI_MODEL)
chat = model.start_chat()
chat.send_message(prompt)

p = pyaudio.PyAudio()
output = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=FRAME_SIZE)

client = texttospeech.TextToSpeechClient()
bd = BackchannelDetector()
gh = GestureHandler()
def signal_handler(sig, frame):
    gh.clearQueue()
    gh.addToQueue("neutral")
    while not gh.isQueueEmpty():
        time.sleep(0.05)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def backchannel_callback():
    print("backchannel!")
    gh.addToQueue("idle")

text_to_speech(client, output, "quack")
gh.start()

with open('fillers.txt') as f:
    fillers = f.read().splitlines()

if args.intro:
    intro = llm_respond(chat, "Introduce yourself!")
    speak_length = text_to_speech(client, output, intro)
    time.sleep(speak_length)

while True:
    if args.text: text = input("Input: ")
    else:
        bd.start(backchannel_callback)
        text = speech_to_text()
        bd.stop()
        gh.clearQueue()

    try: 
        responses = llm_respond(chat, text)
        for response in responses:
            if args.text: print("Output: " + response)
            else:
                print(response)
                speak_length = text_to_speech(client, output, response)
                gh.gestureForSpeaking(response, speak_length)
                time.sleep(speak_length)
    except:
        continue