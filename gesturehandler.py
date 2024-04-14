import threading
import time
import gesticulator
from embodiment import Embodiment

class GestureHandler:

    def __init__(self):
        self.action_queue = []
        self.running = False
        self.body = Embodiment()

    def getGestures(self):
        return ["neutral", "talk1", "talk2"]

    def addToQueue(self, action):
        self.action_queue.append(action)
    
    def clearQueue(self):
        self.action_queue = []

    def start(self):
        self.t = threading.Thread(target = self.__run)
        self.t.setDaemon(True)
        self.running = True
        self.t.start()

    def __run(self):
        while self.running:
            #print("hi!")
            if len(self.action_queue) == 0:
                time.sleep(0.01)
                continue
            action_func = getattr(gesticulator, self.action_queue[0])
            self.action_queue.pop(0)
            action_thread = threading.Thread(target=action_func, args=(self.body,))
            action_thread.setDaemon(True)
            action_thread.start()
            action_thread.join()

    def stop(self):
        self.running = False
        self.t.join()

if __name__ == "__main__":
    gh = GestureHandler()
    gh.start()
    gh.addToQueue("talk1")
    #time.sleep(1)
    gh.addToQueue("talk2")
    #time.sleep(1)
    gh.addToQueue("talk1")
    #time.sleep(1)
    gh.addToQueue("talk2")
    #time.sleep(1)
    gh.addToQueue("talk1")
    #time.sleep(1)
    gh.addToQueue("talk2")
    #time.sleep(1)
    time.sleep(5)
    gh.addToQueue("neutral")
    time.sleep(0.5)
    gh.stop()