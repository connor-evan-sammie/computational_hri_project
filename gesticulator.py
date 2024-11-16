import time
import numpy as np
import scipy
import platform
if platform.system() == "Windows":
    from matplotlib import pyplot as plt

#Left, right, yaw, pitch
neutral_coords = np.array([0, 0, 0, 0])
idle_coords = np.array([[-30, 150], [-30, 150], [-45, 45], [-30, 40]])

thinking1_coords = np.array([120, -10, -30, -15])
thinking2_coords = np.array([-10, 120, 30, -15])
exclaim_coords = np.array([45, 45, 10, 15])
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
    if len(pose.shape) > 1:
        new_pose = np.zeros((4,))
        for i in range(4):
            new_pose[i] = np.random.randint(pose[i, 0], pose[i, 1]+1, None)
        print(f"Random coords: {new_pose}")
    else:
        new_pose = pose
    points = spline(curr_pose, new_pose, N)
    for i in range(points.shape[0]):
        #print(points[i, :])
        body.setPose(points[i, :])
        time.sleep(dt)

def thinking(body):
    print("Going to thinking...")
    which = np.random.randint(0, 2)
    if which == 0:
        toSimplePose(body, thinking1_coords, N, T)
    elif which == 1:
        toSimplePose(body, thinking2_coords, N, T)

def exclaim(body):
    print("Going to ahah...")
    toSimplePose(body, exclaim_coords, N=N, T=0.25)

def chatty(body):
    neutral(body)
    chatty_t = 0.25
    toSimplePose(body, [-30,30, 10, 0], N=N, T=chatty_t)
    toSimplePose(body, [30,-30, -5, 0], N=N, T=chatty_t)
    toSimplePose(body, [-30,30, 10, 0], N=N, T=chatty_t)
    toSimplePose(body, [30,-30, -5, 0], N=N, T=chatty_t)

def inquire(body):
    inquire_t = 1
    toSimplePose(body, [-30,30, 20, 0], N=N, T=inquire_t)

def sigh(body): 
    curr_pose = body.getPose()
    toSimplePose(body, np.array([10, 10, 5, 0]) + curr_pose, N=N, T=0.5)
    toSimplePose(body, [-30, -30, -15, 0], N=N, T=1)

def lightbulb(body):
    toSimplePose(body, [90, 0, 10, 0], N=N, T=0.25)

def affirmative_nod(body):
    toSimplePose(body, [0, 0, -30, 0], N=N, T=0.5)
    neutral(body)

def slow_nod(body):
    toSimplePose(body, [0, 0, -30, 0], N=N, T= 1)
    neutral(body)

def curt_nod(body):
    toSimplePose(body, [0, 0, -30, 0], N=N, T= 0.25)
    neutral(body)

def repetitive_nod(body):
    affirmative_nod(body)
    affirmative_nod(body)
    affirmative_nod(body)

def horizontal_nod(body):
    curr_pose = body.getPose()
    toSimplePose(body, np.array([0, 0, -5, 30]) + curr_pose, N=N, T= 0.25)
    toSimplePose(body, np.array([0, 0, -10, -20]) + curr_pose, N=N, T= 0.25)
    toSimplePose(body, np.array([0, 0, -15, 10]) + curr_pose, N=N, T= 0.25)
    toSimplePose(body, np.array([0, 0, -20, 0]) + curr_pose, N=N, T= 0.25)
    
def snap_neutral(body):
    print("Going to snap_neutral...")
    body.setPose(neutral_coords)

def neutral(body):
    print("Going to neutral...")
    toSimplePose(body, neutral_coords, N=N, T=T)
