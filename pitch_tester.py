import pyaudio
import wave
#import pickle

# Settings for the audio recording
FORMAT = pyaudio.paInt16  # Format for the audio, 16-bit
CHANNELS = 1              # Number of channels, 1 for mono, 2 for stereo
RATE = 44100              # Sample rate (44.1kHz)
CHUNK = 1024              # Number of audio frames per buffer
RECORD_SECONDS = 10       # Duration to record (in seconds)
OUTPUT_FILENAME = "output.wav"  # Name of the output WAV file

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished.")

stream.stop_stream()
stream.close()
audio.terminate()

with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"File saved as {OUTPUT_FILENAME}")
