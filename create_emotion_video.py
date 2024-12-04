from AffectNet.deployment.tensorflow_detector import *
from headpose.detect import PoseEstimator
import cv2
import threading
import time
from matplotlib import pyplot as plt
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import numpy as np

PATH_TO_CKPT = './AffectNet/deployment/frozen_graphs/frozen_inference_graph_face.pb'
PATH_TO_CLASS = './AffectNet/deployment/frozen_graphs/classificator_full_model.pb'
PATH_TO_REGRESS = './AffectNet/deployment/frozen_graphs/regressor_full_model.pb'
detector = TensorflowDetector(PATH_TO_CKPT, PATH_TO_CLASS, PATH_TO_REGRESS)
cap = cv2.VideoCapture("videos/emotion_cycling.mp4")
valences = []
arousals = []
emotions = []
num_frames = 0
running = True
while(running):
    print(num_frames)
    ret, frame = cap.read()
    print(ret)
    if not ret:
        running = False
        continue
    num_frames += 1
    frame = frame[:, 250:1050, :]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    valence, arousal, emotions_detected = detector.run(frame)
    valence = valence[0]
    arousal = arousal[0]
    emotions_detected = emotions_detected[0]
    print(f"Valence: {valence}, Arousal: {arousal}, Emotion: {emotions_detected}")
    valences.append(valence)
    arousals.append(arousal)
    emotions.append(emotions)

print("Ding!")
print(arousals)
arousals = np.array(arousals)
valences = np.array(valences)
emotions = np.array(emotions)

print("Dang!")
np.save("videos/arousals.npy", arousals)
np.save("videos/valences.npy", valences)
np.save("videos/emotions.npy", emotions)
print(f"Num frames: {num_frames}")

print("yeet")
cap.release()

print("dont")