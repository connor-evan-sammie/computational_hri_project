import time
import numpy as np
import scipy.interpolate
import platform
if platform.system() == "Windows":
    from matplotlib import pyplot as plt

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
