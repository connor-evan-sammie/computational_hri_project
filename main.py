from pitch_detector import PitchDetector
from face_handler import FaceHandler
from backchannel_mdp import BackchannelMDP
#from embodiment import Embodiment
from gesturehandler import GestureHandler
import time

if __name__ == "__main__":
    def gesture_callback(gesture):
        pass

    duck = GestureHandler(gesture_callback)

    def mdp_callback(action):
        print(action)
        duck.addToQueue(action)

    mdp = BackchannelMDP(mdp_callback)

    def pitch_callback(pitch):
        #print(f"Pitch: {pitch}")
        mdp.set_speech_measurements(pitch)

    def face_callback(face):
        #print(f"Face: {face.T}")
        mdp.set_face_measurements(face)

    pitch_detector = PitchDetector(pitch_callback)
    face_handler = FaceHandler(face_callback)

    pitch_detector.start()
    face_handler.start()
    duck.start()

    input()

    pitch_detector.stop()
    face_handler.stop()
    duck.stop()

