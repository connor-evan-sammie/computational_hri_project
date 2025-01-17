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
pose_coords = np.array([[-30, 150], [-30, 150], [-45, 45], [-30, 40]])

idle_coords = np.array([[-10, 10], [-10, 10], [-5, 5], [0, 10]])

thinking1A_coords = np.array([120, -10, -30, -10])
thinking1B_coords = np.array([110, -5, -25, -20])
thinking2A_coords = np.array([-10, 120, 30, -10])
thinking2B_coords = np.array([-5, 110, 25, -20])

chattyA_coords = np.array([-15, 15, 0, 15])
chattyB_coords = np.array([15, -15, 0, 5])

inquire1_coords = np.array([[0, 0], [0, 0], [-10, 10], [25, 25]])

nodA_coords = np.array([0, 0, 0, 10])
nodB_coords = np.array([10, 10, 0, -5])

ahah1_coords = np.array([[75, 125], [75, 125], [0, 0], [26, 30]])

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
    else:
        new_pose = pose
    points = spline(curr_pose, new_pose, N)
    for i in range(points.shape[0]):
        body.setPose(points[i, :])
        time.sleep(dt)

def talk1(body, N=N, T=T):
    toSimplePose(body, talk1_coords, N, T)

def talk2(body, N=N, T=T):
    toSimplePose(body, talk2_coords, N, T)

def talk3(body, N=N, T=T):
    toSimplePose(body, talk3_coords, N, T)

def talk4(body, N=N, T=T):
    toSimplePose(body, talk4_coords, N, T)

def rand(body, N=N, T=T):
    toSimplePose(body, pose_coords, N, 1.5*np.random.rand()+0.1)

def idle(body, args=None):
    toSimplePose(body, idle_coords, N, np.random.rand()/2.0+1)

def thinking(body, N=N, T=T):
    which = np.random.randint(0, 2)
    if which == 0:
        toSimplePose(body, thinking1A_coords, N, T)
    elif which == 1:
        toSimplePose(body, thinking2A_coords, N, T)

def ahah1(body):
    toSimplePose(body, ahah1_coords, N=N, T=0.25)

def snap_neutral(body):
    body.setPose(neutral_coords)

def neutral(body, duration = 0, T=T):
    toSimplePose(body, neutral_coords, N=N, T=T)
    time.sleep(duration)

def question(body, args):
    duration = args[0]
    toSimplePose(body, inquire1_coords, N=N, T=min(duration, 1))

def exclaim(body, args):
    duration = args[0]
    wait_time = 0
    if len(args) == 2:
        wait_time = args[1]
    #if duration < 1:
    wing_angle = np.random.randint(75, 125, None)
    toSimplePose(body, np.array([wing_angle, wing_angle, 0, 26]), N=N, T=min(duration, 0.2))
    time.sleep(wait_time)

def declare_thinking(body, args):
    duration = args[0]
    wobble_duration = min(1, duration)
    which = np.random.randint(0, 2)
    cycles = max(int(duration // wobble_duration), wobble_duration)
    for i in range(cycles):
        if i % 2 == 0 and which == 0:
            toSimplePose(body, thinking1A_coords, N=N, T=wobble_duration)
        elif i % 2 == 0 and which == 1:
            toSimplePose(body, thinking2A_coords, N=N, T=wobble_duration)
        elif i % 2 == 1 and which == 0:
            toSimplePose(body, thinking1B_coords, N=N, T=wobble_duration)
        elif i % 2 == 1 and which == 1:
            toSimplePose(body, thinking2B_coords, N=N, T=wobble_duration)

def declare_chatty(body, args):
    duration = args[0]
    wobble_duration = min(0.6, duration)
    cycles = max(int(duration // wobble_duration), wobble_duration)
    for i in range(cycles):
        if i % 2 == 0:
            toSimplePose(body, chattyA_coords, N=N, T=wobble_duration)
            #time.sleep(wobble_duration/3)
        if i % 2 == 1:
            toSimplePose(body, chattyB_coords, N=N, T=wobble_duration)
            #time.sleep(wobble_duration/3)

def declare(body, args):
    which = np.random.randint(0, 2)
    if which == 0:
        declare_thinking(body, args)
    elif which == 1:
        declare_chatty(body, args)

def nod(body):
    nod_duration = 0.4
    toSimplePose(body, nodA_coords, N=N, T=nod_duration)
    toSimplePose(body, nodB_coords, N=N, T=nod_duration)
    toSimplePose(body, nodA_coords, N=N, T=nod_duration)

def listening(body):
    which = np.random.randint(0, 4)
    if which == 0:
        nod(body)
    elif which == 1:
        declare_chatty(body, (1.25,))
    elif which == 2:
        declare_thinking(body, (3,))

def testing(body, args):
    print("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY")
    print(args[0])