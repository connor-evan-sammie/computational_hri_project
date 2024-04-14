import time
import numpy as np
from scipy.interpolate import CubicSpline
import scipy

neutral_coords = np.array([0, 0, 0, 0])
talk1_coords = np.array([150, 150, 0, 10])
talk2_coords = np.array([130, 130, 0, -10])

talk3_coords = np.array([150, 130, 0, 10])
talk4_coords = np.array([130, 150, 0, -10])
N = 15
dt = 0.04

def spline(p1, pf, N, type="cubic"):
    sp = scipy.interpolate.interp1d(np.array([-(N-1), 0, N-1, 2*(N-1)]), np.vstack((pf, p1, pf, p1)).T, kind=type, axis=1)
    points = sp(np.arange(1, N)).T
    print(points)
    #points = np.linspace(p1, pf, N, axis=0)[1:, :]
    return points

def talk1(body):
    curr_pose = body.getPose()
    points = spline(curr_pose, talk3_coords, N)
    print("going to talk 1...")
    for i in range(points.shape[0]):
        #print(points[i, :])
        body.setPose(points[i, :])
        time.sleep(dt)

def talk2(body):
    curr_pose = body.getPose()
    points = spline(curr_pose, talk4_coords, N)
    print("going to talk 2...")
    for i in range(points.shape[0]):
        #print(points[i, :])
        body.setPose(points[i, :])
        time.sleep(dt)



def neutral(body):
    body.setPose(neutral_coords)

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