import sounddevice as sd
import numpy as np
import crepe
import time
import matplotlib.pyplot as plt
from queue import Queue

# Parameters
sample_rate = 16000  # Sample rate for audio input
buffer_duration = 0.5  # Duration of audio buffer in seconds
queue = Queue()

# Callback function to process audio stream
def audio_callback(indata, frames, time, status):
    queue.put(indata.copy())

# Function to analyze pitch using CREPE
def analyze_pitch(audio_data):
    _, frequency, confidence, _ = crepe.predict(audio_data, sample_rate, viterbi=True)
    return frequency, confidence

# Start the audio stream
stream = sd.InputStream(callback=audio_callback, channels=2, samplerate=sample_rate, dtype=np.int16)
stream.start()

frequencies = []

print("Recording... Press Ctrl+C to stop.")
try:
    while True:
        if not queue.empty():
            audio_chunk = queue.get()
            audio_chunk = audio_chunk.flatten()
            print(audio_chunk)

            # Analyze pitch
            frequency, confidence = analyze_pitch(audio_chunk)
            frequencies.extend(frequency)

            # Plot the results
            plt.plot(frequencies)
            plt.pause(0.01)
            plt.clf()

            # Print the result
            print(frequency)
            print(f"Frequency: {frequency.mean():.2f} Hz, Confidence: {confidence.mean():.2f}")

        time.sleep(buffer_duration)
except KeyboardInterrupt:
    print("Stopped.")
finally:
    stream.stop()