import time
import numpy as np
import scipy.interpolate
import platform
if platform.system() == "Windows":
    from matplotlib import pyplot as plt
import soundfile as sf
import numpy as np
import pyaudio

from scipy.signal import resample


# Example usage
#file_path = "path_to_your_file.wav"  # Replace with the path to your .wav file
#play_wav(file_path, volume=70)  # Adjust volume as needed (0-100)


#Left, right, yaw, pitch
neutral_coords = np.array([0, 0, 0, 0])
idle_coords = np.array([[-30, 150], [-30, 150], [-45, 45], [-30, 40]])

thinking1_coords = np.array([120, -10, -30, -15])
thinking2_coords = np.array([-10, 120, 30, -15])
exclaim_coords = np.array([60, 60, 0, 15])
sad1_coords = np.array([-15, -15, 10, -20])

T = 0.5
N = 100

#dt = 0.04
dt = T/N
def spline(p1, pf, N, type="cubic"):
    sp = scipy.interpolate.interp1d(np.array([-(N/2), 0, N-1, 3*N/2]), np.vstack((pf, p1, pf, p1)).T, kind=type, axis=1)
    points = sp(np.arange(1, N)).T
    return points

def toSimplePose(body, pose, N, T):
    dt = T/N
    curr_pose = body.getPose()
    new_pose = pose
    if type(pose) == type([]):
        new_pose = np.array(pose)
    points = spline(curr_pose, new_pose, N)
    for i in range(points.shape[0]):
        #print(points[i, :])
        body.setPose(points[i, :])
        time.sleep(dt)

def thinking(body):
    toSimplePose(body, thinking1_coords, N, T)
    time.sleep(0.75)
    neutral(body, time=0.75)

def exclaim(body):
    toSimplePose(body, exclaim_coords, N=N, T=0.15)
    time.sleep(0.75)
    neutral(body, time=0.3)

def chatty(body):
    neutral(body)
    chatty_t = 0.25
    toSimplePose(body, [-30,30, 0, 10], N=N, T=chatty_t)
    toSimplePose(body, [30,-30, 0, -5], N=N, T=chatty_t)
    toSimplePose(body, [-30,30, 0, 10], N=N, T=chatty_t)
    toSimplePose(body, [30,-30, 0, -5], N=N, T=chatty_t)
    neutral(body, chatty_t)

def inquire(body):
    inquire_t = 1
    toSimplePose(body, [-10,-10, 0, 30], N=N, T=inquire_t)

def sigh(body): 
    curr_pose = body.getPose()
    toSimplePose(body, np.array([10, 10, 0, 5]) + curr_pose, N=N, T=0.5)
    toSimplePose(body, [-30, -30, 0, -15], N=N, T=1)
    time.sleep(0.75)
    neutral(body, time=0.75)

def lightbulb(body):
    toSimplePose(body, [90, 0, 0, 10], N=N, T=0.1)
    time.sleep(0.5)
    neutral(body, time=0.5)

def affirmative_nod(body):
    toSimplePose(body, [0, 0, 0, -30], N=N, T=0.4)
    neutral(body, time=0.4)

def slow_nod(body):
    toSimplePose(body, [0, 0, 0, -30], N=N, T= 1)
    neutral(body, time=1)

def curt_nod(body):
    toSimplePose(body, [0, 0, 0, -30], N=N, T= 0.15)
    neutral(body, time=0.15)

def repetitive_nod(body):
    affirmative_nod(body)
    affirmative_nod(body)
    affirmative_nod(body)

def horizontal_nod(body):
    curr_pose = body.getPose()
    toSimplePose(body, np.array([0, 0, 30, -10]) + curr_pose, N=N, T= 0.25)
    toSimplePose(body, np.array([-4, -4, -20, -15]), N=N, T= 0.25)
    toSimplePose(body, np.array([-8, -8, 10, -20]), N=N, T= 0.25)
    toSimplePose(body, np.array([-16, -16, 0, -25]), N=N, T= 0.25)
    time.sleep(0.25)
    neutral(body, time=0.5)
    
def snap_neutral(body):
    body.setPose(neutral_coords)

def neutral(body, time = T):
    toSimplePose(body, neutral_coords, N=N, T=time)

p = pyaudio.PyAudio()

# Get the device index by name
device_name="UACDemoV1.0: USB Audio (hw:2,0)"
device_index = None
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if device_name and device_name in info['name']:
        device_index = i
        break

def play_wav(filepath, volume=1.0, desired_samplerate=48000, desired_channels=1):
    """
    Plays a .wav file through a USB speaker with volume adjustment.

    Parameters:
    - filepath: path to the .wav file.
    - volume: volume level (0.0 to 1.0).
    - device_name: name or index of the audio output device.
    - desired_samplerate: desired sampling rate for the device.
    - desired_channels: desired number of audio channels for the device.
    """
    # Read the .wav file
    data, original_samplerate = sf.read(filepath, dtype='float32')

    # Adjust volume
    data *= volume

    # Resample if original sample rate is different from the desired one
    if original_samplerate != desired_samplerate:
        print(f"Resampling from {original_samplerate}Hz to {desired_samplerate}Hz")
        num_samples = int(len(data) * float(desired_samplerate) / original_samplerate)
        data = resample(data, num_samples)


    if device_index is None:
        raise ValueError("Specified device not found. Please check the device name.")

    # Try to open the stream using desired settings
    try:
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=desired_channels,
            rate=desired_samplerate,
            output=True,
            output_device_index=device_index
        )
    except Exception as e:
        print(f"Failed to open stream with desired settings: {e}")
        p.terminate()
        return

    # Play the sound
    chunk_size = 1024
    num_chunks = (len(data) + chunk_size - 1) // chunk_size  # Calculate number of chunks
    for start in range(num_chunks):
        end = min(len(data), (start + 1) * chunk_size)
        stream.write(data[start * chunk_size:end].tobytes())
    
    # Wait for playback to finish
    stream.stop_stream()
    
    # Close the stream
    stream.close()

def mhm(body):
    play_wav("./sounds/mhm.wav", 0.6)

def gotcha(body):
    play_wav("./sounds/gotcha.wav", 0.6)

def quack(body):
    play_wav("./sounds/quack.wav", 0.6)

def ahh(body):
    play_wav("./sounds/ahh.wav", 0.6)

def hmmmmm(body):
    play_wav("./sounds/hmmmmm.wav", 0.6)

if __name__ == "__main__":
    mhm(None)
    ahh(None)
    gotcha(None)
    quack(None)
    hmmmmm(None)