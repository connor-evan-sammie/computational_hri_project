import random
import threading
import wave
import time
import signal
import sys

import numpy as np
import mdptoolbox as mdp_tb

class BackchannelMDP:
    
    def __init__(self):
        
        self.P = 0
        self.R = 0
        
        # ========= State Vector Syntax =================
        # 
        #           S0 = Valence (-1.0, 1.0) [5]
        #           S1 = Activation (-1.0, 1.0) [5]
        #    S =    S2 = Roll (-35.0, 35.0) [3]
        #           S3 = Pitch (-35.0, 45.0) [5]
        #           S4 = Inflection (-1.0, 1.0) [3]
        #           
        # =============================================
        
        
        
        self.callback = callback
        self.running = False
        
    def _run(self):
        
        
        vi = mdp_tb.mdp.ValueIteration(P, R, 0.9)
        vi.run()
        
        self.callback()
        
        
    def start(self):
        if self.running is False:
            self.running = True
            self.running_thread = threading.Thread(None, self._run_helper)
            self.running_thread.daemon = True
            self.running_thread.start()
    
    def stop(self):
        self.running = False
        self.running_thread.join()