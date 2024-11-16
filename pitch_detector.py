import aubio
import numpy as np
import pyaudio
import sys
import time
import scipy.signal
import threading

class PitchDetector:
    def __init__(self, callback):
        BUFFER_SIZE             = 4096
        CHANNELS                = 1
        FORMAT                  = pyaudio.paFloat32
        METHOD                  = "default"
        SAMPLE_RATE             = 44100
        HOP_SIZE                = BUFFER_SIZE//2
        self.PERIOD_SIZE_IN_FRAME    = HOP_SIZE
        self.pA = pyaudio.PyAudio()
        self.mic = self.pA.open(format=FORMAT, channels=CHANNELS,
            rate=SAMPLE_RATE, input=True,
            frames_per_buffer=self.PERIOD_SIZE_IN_FRAME)
        self.pDetection = aubio.pitch(METHOD, BUFFER_SIZE, HOP_SIZE, SAMPLE_RATE)
        self.pDetection.set_unit("Hz")
        self.pDetection.set_silence(-60)
        self.b, self.a = scipy.signal.butter(3, 1000/SAMPLE_RATE, 'lowpass')
        self.running = False
        self.callback = callback

    def start(self):
        self.t = threading.Thread(target = self.__run)
        self.t.setDaemon(True)
        self.running = True
        self.t.start()

    def __run(self):
        while self.running:
            data = self.mic.read(self.PERIOD_SIZE_IN_FRAME)
            samples = np.fromstring(data, dtype=aubio.float_type)
            samples = scipy.signal.lfilter(self.b, self.a, samples)
            samples = samples.astype(np.float32)
            pitch = self.pDetection(samples)[0]
            self.callback(pitch)


    
    def stop(self):
        self.running = False
        self.t.join()
    
    #def __del__(self):
    #    self.stop()

if __name__ == "__main__":
    bd = PitchDetector(lambda pitch: print(pitch))
    bd.start()
    time.sleep(5)
    bd.stop()