import sounddevice as sd
import numpy as np
import crepe
import time
import matplotlib.pyplot as plt
import threading
from scipy.io import wavfile
sr, audio = wavfile.read('oxp.wav')
time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)


sample_rate = 16000  # Sample rate for audio input
buffer_duration = 0.5  # Duration of audio buffer in seconds

stream = sd.InputStream(channels=2, samplerate=sample_rate, dtype=np.float32)
out = sd.OutputStream(samplerate=sample_rate, channels=2, dtype=np.float32)

stream.start()
out.start()

#data, overflowed = stream.read(1024*8)
#out.write(data)
frequencies = []
threads = []

def process_audio(data):
    _, frequency, confidence, _ = crepe.predict(data, sample_rate, viterbi=True)
    frequencies.extend(frequency[confidence > 0.5])
    #frequencies.extend(confidence)
while True:
    data, overflowed = stream.read(2048)
    print(data.shape)
    #_, frequency, confidence, _ = crepe.predict(data, sample_rate, viterbi=True)
    #frequencies.append(frequency)
    threads.append(threading.Thread(None, process_audio, args = (data,)))
    threads[-1].Daemon = True
    threads[-1].start()
    if len(frequencies) > 0:
        plt.plot(frequencies)
        plt.pause(0.01)
        plt.clf()


stream.stop()
out.stop()

#plt.plot(data)
#plt.show()
#_, frequency, confidence, _ = crepe.predict(data, sample_rate, viterbi=True)
#print(frequency)