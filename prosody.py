import crepe
import pyaudio
from scipy.io import wavfile
import io
import wave
import numpy as np

container = io.BytesIO()

sr, audio = wavfile.read('oxp.wav')
#time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)

print(type(audio[0, 0]))
"""
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024*2
RECORD_SECONDS = 1

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()
stream.close()
audio.terminate()

#print(frames)
#time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)

waveFile = wave.open(container, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))

container.seek(0)
data_package = container.read()

print(frames)
my_data = np.array(frames)#[int.from_bytes(frames[0][i:i+2], 'big') for i in range(len(frames[0])-1)]


#time, frequency, confidence, activation = crepe.predict(my_data, RATE, viterbi=True)
#print(frequency)
"""