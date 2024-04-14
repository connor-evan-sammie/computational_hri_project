import time
import numpy as np
import scipy
import platform
if platform.system() == "Windows":
    from matplotlib import pyplot as plt

neutral_coords = np.array([0, 0, 0, 0])
talk1_coords = np.array([150, 150, 0, 10])
talk2_coords = np.array([130, 130, 0, -10])

talk3_coords = np.array([150, 130, 0, 10])
talk4_coords = np.array([130, 150, 0, -10])
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
    points = spline(curr_pose, pose, N)
    for i in range(points.shape[0]):
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

def neutral(body):
    print("Going to neutral...")
    body.setPose(neutral_coords)
