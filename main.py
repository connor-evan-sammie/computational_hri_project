import speech_recognition as sr
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
from google.cloud import texttospeech
import pyaudio

GOOGLE_CLOUD_SPEECH_CREDENTIALS = "./creds/speechtotext.json"

prompt = """You are an AI rubber duck designed to help computer science students at the University of Michigan in their studies. Your role is to help the students learn by helping them debug their code. You will not provide a solution to their problem but rather help them to learn. You will not prompt them for their code. All user input will be provided to you using speech to text software. Respond in shorter messages (still using grammatically correct english) that can be spoken aloud using text to speech software."""

vertexai.init(project="duck-414417", location="us-central1")
model = GenerativeModel("gemini-1.0-pro")
chat = model.start_chat()
chat.send_message(prompt)

p = pyaudio.PyAudio()
output = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)

client = texttospeech.TextToSpeechClient()

def speech_to_text():
    print("Recognizing speech...")
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=1)
        audio = rec.listen(source)
        text = rec.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
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
        name='en-US-Journey-F',
        language_code="en-US", 
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
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

while True:
    text = speech_to_text()
    response = llm_respond(chat, text)
    text_to_speech(client, output, response)