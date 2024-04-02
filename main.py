import speech_recognition as sr
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
from google.cloud import texttospeech
import pyaudio

PROJECT_ID = "duck-414417"
GOOGLE_CLOUD_SPEECH_CREDENTIALS = "./creds/speechtotext.json"

AI_MODEL = "gemini-1.0-pro"
VOICE_MODEL = "en-US-Journey-F"
FRAME_SIZE = 4096

def speech_to_text():
    print("Recognizing speech...")
    rec = sr.Recognizer()
    rec.energy_threshold = 300
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=1)
        audio = rec.listen(source)
        try:
            text = rec.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        except:
            print("No audio recognized!")
            return ""
        return text
    return ""

def llm_respond(model, input_text):
    print("Using LLM to generate response...")
    print("Input: " + input_text)
    text_response = []
    responses = chat.send_message(input_text, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)
    return response.text

def text_to_speech(client, output, input_text):
    print("Speaking...")
    print("Output: " + input_text)
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

vertexai.init(project=PROJECT_ID, location="us-central1")
model = GenerativeModel(AI_MODEL)
chat = model.start_chat()
chat.send_message(prompt)

p = pyaudio.PyAudio()
output = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=FRAME_SIZE)

client = texttospeech.TextToSpeechClient()

while True:
    text = speech_to_text()
    response = llm_respond(chat, text)
    text_to_speech(client, output, response)