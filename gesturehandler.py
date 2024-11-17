import threading
import time
import gesticulator
from embodiment import Embodiment as body

class GestureHandler:

    def __init__(self):
        self.action_queue = []
        self.running = False
        self.body = body()

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
            action_func = getattr(gesticulator, self.action_queue[0])
            action_func(self.body)
            self.action_queue.pop(0)
            #action_thread = threading.Thread(target=action_func, args=(self.body,))
            #action_thread.daemon = True
            #action_thread.start()
            #action_thread.join()

    def stop(self):
        self.running = False
        self.t.join()

if __name__ == "__main__":
    gh = GestureHandler()
    gh.start()
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
    time.sleep(60)
    gh.stop()

#2p 3y 14l 15r