import time
import numpy as np

neutral_coords = np.array([0, 0, 0, 0])
talk1_coords = np.array([150, 150, 0, 10])
talk2_coords = np.array([130, 130, 0, -10])
N = 5
dt = 0.1

def spline(p1, pf, N):
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #print(pf)
    left = np.linspace(p1[0], pf[0], N)[1:, None]
    right = np.linspace(p1[1], pf[1], N)[1:, None]
    yaw = np.linspace(p1[2], pf[2], N)[1:, None]
    pitch = np.linspace(p1[3], pf[3], N)[1:, None]
    points = np.hstack((left, right, yaw, pitch))
    return points

def talk1(body):
    curr_pose = body.getPose()
    points = spline(curr_pose, talk1_coords, N)
    print("going to talk 1...")
    for i in range(points.shape[0]):
        #print(points[i, :])
        body.setPose(points[i, :])
        time.sleep(dt)

def talk2(body):
    curr_pose = body.getPose()
    points = spline(curr_pose, talk2_coords, N)
    print("going to talk 2...")
    for i in range(points.shape[0]):
        body.setPose(points[i, :])
        print(points[i, :])
        time.sleep(dt)

def neutral(body):
    body.setPose(neutral)

"""
def who():
    phrase = "the Who(tm) gesture"
    for c in phrase:
        print(c, end="", flush="True")
        time.sleep(0.1)
    print()

def what():
    phrase = "the What(tm) gesture"
    for c in phrase:
        print(c, end="", flush="True")
        time.sleep(0.1)
    print()

def when():
    phrase = "the When(tm) gesture"
    for c in phrase:
        print(c, end="", flush="True")
        time.sleep(0.1)
    print()

def where():
    phrase = "the Where(tm) gesture"
    for c in phrase:
        print(c, end="", flush="True")
        time.sleep(0.1)
    print()

def why():
    phrase = "the Why(tm) gesture"
    for c in phrase:
        print(c, end="", flush="True")
        time.sleep(0.1)
    print()

def how():
    phrase = "the How(tm) gesture"
    for c in phrase:
        print(c, end="", flush="True")
        time.sleep(0.1)
    print()
"""