from AffectNet.deployment.tensorflow_detector import *
import cv2

PATH_TO_CKPT = './AffectNet/deployment/frozen_graphs/frozen_inference_graph_face.pb'
PATH_TO_CLASS = './AffectNet/deployment/frozen_graphs/classificator_full_model.pb'
PATH_TO_REGRESS = './AffectNet/deployment/frozen_graphs/regressor_full_model.pb'

detector = TensorflowDetector(PATH_TO_CKPT, PATH_TO_CLASS, PATH_TO_REGRESS)

img = cv2.imread("test_face.jpg")

detector.run(img)
detector.run(img)
detector.run(img)
detector.run(img)
detector.run(img)
detector.run(img)