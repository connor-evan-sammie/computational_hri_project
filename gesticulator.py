import time
import numpy as np

talk_1 = [150, 150, 0, 10]
talk_2 = [130, 130, 0, -10]
N = 5
dt = 0.1


def talk_1(body):
    curr_pose = body.getPose()
    points = spline(curr_pose, talk_1, N)
    for i in range(len(points)):
        body.setPose(points[i])
        time.sleep(dt)

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