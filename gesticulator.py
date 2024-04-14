import time
import numpy as np
import scipy
import platform
if platform.system() == "Windows":
    from matplotlib import pyplot as plt

#Left, right, yaw, pitch
neutral_coords = np.array([0, 0, 0, 0])
talk1_coords = np.array([150, 150, 0, 10])
talk2_coords = np.array([130, 130, 0, -10])
talk3_coords = np.array([150, 130, 0, 10])
talk4_coords = np.array([130, 150, 0, -10])
idle_coords = np.array([[-30, 150], [-30, 150], [-45, 45], [-30, 40]])

thinking1_coords = np.array([120, -10, -30, -15])
thinking2_coords = np.array([-10, 120, 30, -15])
ahah1_coords = np.array([45, 45, 10, 15])
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

def talk1(body, N=N, T=T):
    print("Going to talk 1...", flush=True)
    toSimplePose(body, talk1_coords, N, T)

def talk2(body, N=N, T=T):
    print("Going to talk 2...", flush=True)
    toSimplePose(body, talk2_coords, N, T)

def talk3(body, N=N, T=T):
    print("Going to talk 3...", flush=True)
    toSimplePose(body, talk3_coords, N, T)

def talk4(body, N=N, T=T):
    print("Going to talk 4...", flush=True)
    toSimplePose(body, talk4_coords, N, T)

def rand(body, N=N, T=T):
    print("Going to random idle...", flush=True)
    toSimplePose(body, idle_coords, N, 1.5*np.random.rand()+0.1)

def thinking(body):
    print("Going to thinking...")
    which = np.random.randint(0, 2)
    if which == 0:
        toSimplePose(body, thinking1_coords, N, T)
    elif which == 1:
        toSimplePose(body, thinking2_coords, N, T)

def ahah1(body):
    print("Going to ahah...")
    toSimplePose(body, ahah1_coords, N=N, T=0.25)

def snap_neutral(body):
    print("Going to snap_neutral...")
    body.setPose(neutral_coords)

def neutral(body):
    print("Going to neutral...")
    toSimplePose(body, neutral_coords, N=N, T=T)
