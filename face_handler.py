from AffectNet.deployment.tensorflow_detector import *
from headpose.detect import PoseEstimator
import cv2
import threading
import time
from matplotlib import pyplot as plt
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


PATH_TO_CKPT = './AffectNet/deployment/frozen_graphs/frozen_inference_graph_face.pb'
PATH_TO_CLASS = './AffectNet/deployment/frozen_graphs/classificator_full_model.pb'
PATH_TO_REGRESS = './AffectNet/deployment/frozen_graphs/regressor_full_model.pb'

class FaceHandler():
    def __init__(self, callback):
        """This class runs emotion recognition (valence, arousal, emotion class) from a webcam asyncronously

        Args:
            callback (function): Function that is called every time a frame is processed. Function must take in four positional arguments: valences, arousals, emotions detected, and pose. Each arg will be a list: one entry for each detected face.
        """
        self.callback = callback
        self.detector = TensorflowDetector(PATH_TO_CKPT, PATH_TO_CLASS, PATH_TO_REGRESS)
        self.pose_estimator = PoseEstimator()
        self.running = False
        
        #This pre-run speeds up the process
        self.detector.run(cv2.imread("test_face.jpg"))

    def start(self):
        """Begin automatic capture and emotion recognition.
        """
        if self.running is False:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.running_thread = threading.Thread(None, self._run_helper)
            self.running_thread.daemon = True
            self.running_thread.start()

    def stop(self):
        """Stop automatic capture and emotion recognition.
        """
        self.running = False
        self.running_thread.join()

    def _run_helper(self):
        while self.running:
            ret, img = self.cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                valence, arousal, emotions_detected = self.detector.run(img)
                try:
                    roll, pitch, yaw = self.pose_estimator.pose_from_image(img)
                    pose = [roll, pitch, yaw]
                except ValueError:
                    pose = []
                self.callback(valence, arousal, emotions_detected, pose)
        cv2.VideoCapture(0).release()

if __name__ == "__main__":
    poses = []
    def example_callback(valence, arousal, emotions_detected, pose):
        if len(pose) > 0:
            poses.append(pose)
        print(f"Valences: {valence}, Arousals: {arousal}, Emotions: {emotions_detected}, Pose: {pose}")

    emotions = FaceHandler(example_callback)
    emotions.start()
    time.sleep(120)
    emotions.stop()
    poses = np.array(poses)
    print(poses)
    plt.plot(poses)
    print(f"Roll min: {np.min(poses[:, 0])}")
    print(f"Roll max: {np.max(poses[:, 0])}")
    print(f"Pitch min: {np.min(poses[:, 1])}")
    print(f"Pitch max: {np.max(poses[:, 1])}")
    print(f"Yaw min: {np.min(poses[:, 2])}")
    print(f"Yaw max: {np.max(poses[:, 2])}")
    plt.legend(["roll", "pitch", "yaw"])
    plt.show()

