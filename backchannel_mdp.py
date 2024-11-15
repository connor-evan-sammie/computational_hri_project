import random
import threading
import wave
import time
import signal
import sys

import numpy as np
import mdptoolbox as mdp_tb

class BackchannelMDP:
    
    def __init__(self, callback):
        # ========= Measurements Vector Syntax =================
        # 
        #           M0 = Valence 
        #           M1 = Activation 
        #           M2 = Roll
        #           M3 = Pitch
        #     M =   M4 = p1 
        #           M5 = p2
        #           M6 = p3
        #           M7 = p4
        #           M8 = p5
        #           
        # =============================================
        self.measurements = np.zeros((9,1))
        
        # ========= State Vector Syntax =================
        # 
        #           S0 = Valence        (-1.0, 1.0)     [5]
        #           S1 = Activation     (-1.0, 1.0)     [5]
        #    S =    S2 = Pitch          (-35.0, 45.0)   [5]
        #           S3 = Yaw            (-30.0, 30.0)   [3]
        #           S4 = Inflection     (-1.0, 1.0)     [3]
        #           
        # =============================================
        
        # TODO: state_space is a array of column vectors representing all possible current and future states
        self.state_space = np.zeros((5, 1125))
        
        # TODO: action_space is an array of the possible gestures and responses we can backchannel with
        self.action_space = np.zeros((1, 10))
        
        # current_state represents the column index of the current state in the context of state_space
        self.current_state = 0
        
        
        # MDP values
        self.action_space_size = self.action_space.shape[1]
        self.state_space_size = self.state_space.shape[1]
        
        # TODO: Make these work
        self.P = np.zeros((self.action_space_size, self.state_space_size, self.state_space_size))
        self.R = np.zeros((self.action_space_size, self.state_space_size, self.state_space_size))
        
        # random shit to make the code work
        self.callback = callback
        self.running = False
        
    def _run(self):
        
        # Take in measurements
        # Turn into state
        # Apply MDP to return optimal policy
        # Apply optimal policy to current state to obtain optimal action
        # Publish optimal action
        
        vi = mdp_tb.mdp.ValueIteration(self.P, self.R, 0.9)
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
        
        
    # takes in face measurements and applies them to self.measurements    
    def face_callback(face_measurements):
        pass
    
    # takes in speech measurements and applies them to self.measurements  
    def speech_callback(speech_measurements):
        pass
        
    # measurement is a column vector float of size 9
    # TODO: find closest state to given mesurements and then set current state to this index using self.state_space
    def _measurements_to_state(self, measurement):
    
        self.current_state = 0