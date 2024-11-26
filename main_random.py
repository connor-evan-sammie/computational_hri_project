import time
from gesturehandler import GestureHandler
from random import randrange

if __name__ == "__main__":
    duck = GestureHandler(lambda x: None)
    duck.start()
    action_space = ["neutral",
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
                                      "horizontal_nod",
                                      "mhm",
                                      "ahh",
                                      "hmmmmm",
                                      "gotcha"]
    while True:
        time.sleep(2)
        duck.addToQueue(action_space[randrange(len(action_space))])