#https://gist.github.com/notalentgeek/48aeab398b6b74e3a9134a61b6b79a36

# This is a simple demonstration on how to stream
# audio from microphone and then extract the pitch
# and volume directly with help of PyAudio and Aubio
# Python libraries. The PyAudio is used to interface
# the computer microphone. While the Aubio is used as
# a pitch detection object. There is also NumPy
# as well to convert format between PyAudio into
# the Aubio.
import aubio
import numpy as num
import pyaudio
import sys
import time
from matplotlib import pyplot as plt
import scipy.signal

# Some constants for setting the PyAudio and the
# Aubio.
BUFFER_SIZE             = 2048*2
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
METHOD                  = "default"
SAMPLE_RATE             = 44100
HOP_SIZE                = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE

def main(args):

    # Initiating PyAudio object.
    pA = pyaudio.PyAudio()
    # Open the microphone stream.
    mic = pA.open(format=FORMAT, channels=CHANNELS,
        rate=SAMPLE_RATE, input=True,
        frames_per_buffer=PERIOD_SIZE_IN_FRAME)

    # Initiating Aubio's pitch detection object.
    pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
        HOP_SIZE, SAMPLE_RATE)
    # Set unit.
    pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
    pDetection.set_silence(-60)

    # Infinite loop!
    b, a = scipy.signal.butter(3, 1000, 'lowpass', fs=SAMPLE_RATE)
    t1 = time.time()
    ts = []
    ps = []
    vs = []
    gs = []
    p26s = []
    p26ts = []
    last_silence = time.time()
    last_backchannel = time.time()
    last_percentile_26 = time.time()
    while time.time() - t1 < 15:

        # Always listening to the microphone.
        data = mic.read(PERIOD_SIZE_IN_FRAME)
        # Convert into number that Aubio understand.
        samples = num.fromstring(data,
            dtype=aubio.float_type)
        samples = scipy.signal.lfilter(b, a, samples)
        samples = samples.astype(num.float32)
        # Finally get the pitch.
        pitch = pDetection(samples)[0]
        #pitch = pitch if pitch < 1000 else 1000
        # Compute the energy (volume)
        # of the current frame.
        volume = num.sum(samples**2)/len(samples)
        # Format the volume output so it only
        # displays at most six numbers behind 0.
        volume = "{:6f}".format(volume)

        # Finally print the pitch and the volume.
        #print(str(pitch) + "Hz " + str(volume))
        if pitch > 0.01:
            ts.append(time.time()-t1)
            ps.append(pitch)
            vs.append(volume)
        if pitch < 0.01:
            last_silence = time.time()
        if len(ps) > 2:
            percentile_26 = num.percentile(ps, 26)
            p26s.append(percentile_26)
            p26ts.append(time.time() - t1)
        else:
            percentile_26 = -1
        if pitch > percentile_26:
            last_percentile_26 = time.time()
        P1_P2 = time.time() - last_percentile_26 >= 0.05
        P3 = time.time() - last_silence >= 0.7
        P4 = time.time() - last_backchannel >= 0.8
        print(f"{P1_P2} {P3} {P4}")
        if(P1_P2 and P3 and P4):
            print("GESTURE!!!!!!!!!!!!!!!!!!!!")
            last_backchannel = time.time()
            gs.append(time.time()-t1)
            #ps = []
            #ts = []
            #vs = []


    plt.plot(ts, ps, '.')
    plt.plot(gs, num.zeros((len(gs),)), 'r*')
    plt.plot(p26ts, p26s, 'g--')
    plt.show()


if __name__ == "__main__":
    main(sys.argv)