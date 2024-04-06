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

PROJECT_ID = "duck-414417"
GOOGLE_CLOUD_CREDENTIALS = "./creds.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CLOUD_CREDENTIALS

AI_MODEL = "codechat-bison@002"
LOCATION = "us-central1"
VOICE_MODEL = "en-US-Journey-F"
FRAME_SIZE = 4096

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-t', '--text', action='store_true')

args = parser.parse_args()

def speech_to_text():
    print("Recognizing speech...")
    rec = sr.Recognizer()
    rec.energy_threshold = 300
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=1)
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
    response = chat.send_message(input_text)
    return response.text

def text_to_speech(client, output, input_text):
    print("Speaking...")
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
    output.write(response.audio_content)


with open('prompt.txt', 'r') as file:
    prompt = file.read()

vertexai.init(project=PROJECT_ID, location=LOCATION)
#model = GenerativeModel(AI_MODEL)
model = CodeChatModel.from_pretrained(AI_MODEL)
chat = model.start_chat()
chat.send_message(prompt)

p = pyaudio.PyAudio()
output = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=FRAME_SIZE)

client = texttospeech.TextToSpeechClient()
bd = BackchannelDetector()
gh = GestureHandler()

def backchannel_callback():
    print("gesture!")
    gestures = gh.getGestures()
    i = random.randint(0, len(gestures)-1)
    gh.addToQueue(gestures[i])

gh.start()
while True:
    if args.text: text = input("Input: ")
    else:
        text_to_speech(client, output, "quack!")
        bd.start(backchannel_callback)
        text = speech_to_text()
        bd.stop()
    
    response = llm_respond(chat, text)

    if args.text: print("Output: " + response)
    else: text_to_speech(client, output, response)
