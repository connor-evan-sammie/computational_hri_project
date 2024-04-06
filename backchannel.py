import aubio
import numpy as np
import pyaudio
import sys
import time
import scipy.signal
import threading

class BackchannelDetector:
    def __init__(self):
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
        self.b, self.a = scipy.signal.butter(3, 1000, 'lowpass', fs=SAMPLE_RATE)
        self.running = False

    def start(self, callback = lambda : None):
        t = threading.Thread(target = self.__run, args=(callback,))
        t.setDaemon(True)
        t.start()

    def __run(self, callback):
        ps = []
        last_silence = time.time()
        last_backchannel = time.time()
        last_percentile_26 = time.time()
        last_satisfied = sys.float_info.max
        self.running = True
        while self.running:
            data = self.mic.read(self.PERIOD_SIZE_IN_FRAME)
            samples = np.fromstring(data, dtype=aubio.float_type)
            samples = scipy.signal.lfilter(self.b, self.a, samples)
            samples = samples.astype(np.float32)
            pitch = self.pDetection(samples)[0]
            if pitch > 0.01:
                ps.append(pitch)
            if pitch < 0.01:
                last_silence = time.time()
            if len(ps) > 2:
                percentile_26 = np.percentile(ps, 26)
            else:
                percentile_26 = -1
            if pitch > percentile_26:
                last_percentile_26 = time.time()
            P1_P2 = time.time() - last_percentile_26 >= 0.110
            P3 = time.time() - last_silence >= 0.700
            P4 = time.time() - last_backchannel >= 0.800
            if(P1_P2 and P3 and P4):
                last_satisfied = time.time()
            P5 = time.time() - last_satisfied - 0.700 > 0
            if P5:
                last_satisfied = sys.float_info.max
                last_backchannel = time.time()
                callback()
    
    def stop(self):
        self.running = False

if __name__ == "__main__":
    bd = BackchannelDetector()
    bd.start(lambda: print("Gesture!"))
    time.sleep(10)
    bd.stop()