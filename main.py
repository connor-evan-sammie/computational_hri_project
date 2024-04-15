import os
from ctypes import *
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
import sentence_splitter

PROJECT_ID = "duck-414417"
GOOGLE_CLOUD_CREDENTIALS = "./creds.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CLOUD_CREDENTIALS

AI_MODEL = "codechat-bison@002"
LOCATION = "us-central1"
VOICE_MODEL = "en-US-Journey-F"
FRAME_SIZE = 4096
AUDIO_RATE = 44100

firstrun = True

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-t', '--text', action='store_true')
parser.add_argument('-i', '--intro', action='store_true')
parser.add_argument('-b', '--bypassllm', action='store_true')

args = parser.parse_args()

def speech_to_text():
    rec = sr.Recognizer()
    rec.energy_threshold = 300
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=0.5)
        audio = rec.listen(source)
        try:
            text = rec.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_CREDENTIALS)
        except:
            return ""
        return text
    return ""

def llm_respond(model, input_text):
    global chat
    if len(input_text) == 0: return;
    if args.verbose: print("Input: " + input_text)
    responses = chat.send_message_streaming(input_text)

    part = ""
    sentence_queue = []
    for response in responses:
        part += response.text

        sentences = sentence_splitter.split_into_sentences(part)

        for sentence in sentences:
            if sentence.endswith("!") or sentence.endswith("?") or sentence.endswith("."):
                sentence_queue.append(sentence)
                part = part.replace(sentence, "")

        while len(sentence_queue) != 0: 
            yield sentence_queue.pop(0)

def play_audio(output, wav):
    data = wav.readframes(FRAME_SIZE)
    while data:
        output.write(data)
        data = wav.readframes(FRAME_SIZE)
    wav.close()

def text_to_speech(client, output, input_text):
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


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt): return
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

p = pyaudio.PyAudio()
output = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=FRAME_SIZE)

client = texttospeech.TextToSpeechClient()
bd = BackchannelDetector(verbose=args.verbose)
gh = GestureHandler(verbose=args.verbose)
def signal_handler(sig, frame):
    gh.clearQueue()
    gh.addToQueue("neutral")
    while not gh.isQueueEmpty():
        time.sleep(0.05)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def backchannel_callback():
    #print("backchannel!")
    gh.addToQueue("idle")

text_to_speech(client, output, "quack")
print("Ready!")
gh.start()

with open('fillers.txt') as f:
    fillers = f.read().splitlines()



while True:
    if args.text: 
        bd.start(backchannel_callback)
        text = input("Input: ")
        bd.stop()
        gh.clearQueue()
    else:
        bd.start(backchannel_callback)
        text = speech_to_text()
        bd.stop()
        gh.clearQueue()

    print("user< " + text)
    if text == "END_PROGRAM": break;

    try: 
        responses = llm_respond(chat, text)
        for response in responses:
            print("duck> " + response)
            speak_length = text_to_speech(client, output, response)
            gh.gestureForSpeaking(response, speak_length)
            time.sleep(speak_length)
    except:
        continue
