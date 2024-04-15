import threading
import time
import gesticulator
from embodiment import Embodiment as body

class GestureHandler:

    def __init__(self):
        self.action_queue = []
        self.running = False
        self.body = body()
        self._is_gesticulating = False

    def getBackchannelGestures(self):
        return ["rand", "rand", "rand", "rand", "rand", "talk1", "talk2", "talk3", "talk4"]

    def addToQueue(self, action):
        if(type(action) != type((None,))):
            action = (action,)
        self.action_queue.append(action)

    def gestureForSpeaking(self, sentence, duration):
        if sentence[-1] == "!":
            self.addToQueue(("exclaim", duration))
        elif sentence[-1] == "?":
            self.addToQueue(("question", duration))
        elif sentence[-1] == ".":
            self.addToQueue(("declare", duration))
    
    def clearQueue(self):
        self.action_queue = []

    def isQueueEmpty(self):
        return len(self.action_queue) == 0

    def start(self):
        self.t = threading.Thread(target = self.__run)
        self.t.daemon = True
        self.running = True
        self.t.start()

    def isGesticulating(self):
        return self._is_gesticulating

    def __run(self):
        while self.running:
            if len(self.action_queue) == 0:
                time.sleep(0.01)
                continue
            self._is_gesticulating = True
            top_action = self.action_queue[0]
            top_cmd = top_action[0]
            action_func = getattr(gesticulator, top_cmd)
            self.action_queue.pop(0)
            if len(top_action) == 1:
                action_func(self.body)
            else:
                action_func(self.body, top_action[1:])
            self._is_gesticulating = False

    def stop(self):
        self.running = False
        self.t.join()

if __name__ == "__main__":
    gh = GestureHandler()
    gh.start()
    gh.gestureForSpeaking("What is happening?", 0.1)

    #gh.addToQueue(("testing", 7))
    #for i in range(10):
    #    gh.addToQueue("thinking")
    #gh.addToQueue("thinking")
    #time.sleep(2)
    #gh.addToQueue("ahah1")
    #time.sleep(2)
    #for i in range(60):
    #    gh.addToQueue("rand")
    gh.addToQueue("neutral")
    while not gh.isQueueEmpty():
        time.sleep(0.05)
    gh.stop()

#2p 3y 14l 15r