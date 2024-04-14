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
            self.action_queue.pop(0)
            action_func(self.body)
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
    #for i in range(10):
    #    gh.addToQueue("thinking")
    #gh.addToQueue("thinking")
    #time.sleep(2)
    #gh.addToQueue("ahah1")
    #time.sleep(2)
    for i in range(60):
        gh.addToQueue("rand")
    gh.addToQueue("neutral")
    while not gh.isQueueEmpty():
        time.sleep(0.05)
    gh.stop()

#2p 3y 14l 15r