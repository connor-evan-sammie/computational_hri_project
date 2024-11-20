import threading
import time
import gesticulator
#from embodiment import Embodiment as body
import send_servo_positions

class GestureHandler:

    def __init__(self, gesture_completed_callback):
        self.action_queue = []
        self.running = False
        self.gesture_completed_callback = gesture_completed_callback

    def getBackchannelGestures(self):
        return ["rand", "rand", "rand", "rand", "rand", "talk1", "talk2", "talk3", "talk4"]

    def addToQueue(self, action):
        self.action_queue.append(action)
    
    def clearQueue(self):
        self.action_queue = []

    def isQueueEmpty(self):
        return len(self.action_queue) == 0

    def start(self):
        self.t = threading.Thread(target = self.__run)
        self.t.daemon = True
        self.running = True
        self.t.start()

    def __run(self):
        while self.running:
            if len(self.action_queue) == 0:
                time.sleep(0.01)
                continue
            try:
                send_servo_positions.send_servo_positions(self.action_queue[0])
            except:
                print("Could not connect to duck")
            self.gesture_completed_callback(self.action_queue[0])
            self.action_queue.pop(0)

    def stop(self):
        self.running = False
        self.t.join()

if __name__ == "__main__":
    def gesture_completed_callback(message):
        print(f"Completed {message}")
    gh = GestureHandler(gesture_completed_callback)
    gh.start()
    """
    gs = ["neutral",
            "thinking",
            "chatty",
            "exclaim",
            "inquire",
            "sigh",
            "lightbulb",
            "affirmative_nod",
            "slow_nod",
            "curt_nod",
            "repetitive_nod",
            "horizontal_nod"]
    for i in range(len(gs)):
        gh.addToQueue(gs[i])
    """
    gh.addToQueue("horizontal_nod")
    time.sleep(1)
    gh.stop()

#2p 3y 14l 15r