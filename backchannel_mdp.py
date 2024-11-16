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
        
        # state_space is a array of column vectors representing all possible current and future states
        self.val_states = np.linspace(-1, 1, 5)
        self.aro_states = np.linspace(-1, 1, 5)
        self.pit_states = np.linspace(-35, 45, 5)
        self.yaw_states = np.linspace(-30, 30, 3)
        self.ifl_states = np.linspace(-1, 1, 3)
        grid = np.meshgrid(self.val_states, self.aro_states, self.pit_states, self.yaw_states, self.ifl_states, indexing='ij')
        self.state_space = np.reshape(grid, (5, -1))
        
        # TODO: action_space is an array of the possible gestures and responses we can backchannel with
        self.action_space = np.zeros((1, 20))
        
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
    def set_face_measurements(self, face_measurements):
        self.measurements[0:4] = face_measurements
    
    # takes in speech measurements and applies them to self.measurements  
    def set_speech_measurements(self, speech_measurements):
        self.measurements[4:] = speech_measurements
        
    def _quantize(self, x, bins):
        if x < bins[0]:
            return 0
        for i in range(bins.shape[0]-1):
            midpoint = (bins[i]+bins[i+1])/2
            if bins[i] <= x < bins[i+1] and x <= midpoint:
                return i
            elif bins[i] <= x < bins[i+1] and x > midpoint:
                return i+1
        return bins.shape-1
    
    # Takes in a series of pitches ordered chronologically and returns the concavity (-1, 0, or 1) based on a threshold limit
    def _get_inflection_idx(self, pitches):
        xs = np.arange(0, pitches.shape[0])
        fit = np.polyfit(xs, pitches, 2)
        quadratic_term = fit[0]
        linear_term = fit[1]
        concavity_limit = 0.1

        if abs(quadratic_term) < 0.01:
            return 1 if linear_term > concavity_limit else (-1 if linear_term < -concavity_limit else 0)
        if quadratic_term < -concavity_limit:
            ifl = 0
        elif -concavity_limit <= quadratic_term <= concavity_limit:
            ifl = 1
        else:
            ifl = 2
        return ifl
    
    # measurement is a column vector float of size 9
    # find closest state to given mesurements and then set current state to this index using self.state_space
    def _measurements_to_state(self, measurement):

        val_idx = self._quantize(measurement[0], self.val_states)
        aro_idx = self._quantize(measurement[1], self.aro_states)
        pit_idx = self._quantize(measurement[2], self.pit_states)
        yaw_idx = self._quantize(measurement[3], self.yaw_states)
        ifl_idx = self._get_inflection_idx(np.flip(measurement[4:]))
        
        n_aro = self.aro_states.shape[0]
        n_pit = self.pit_states.shape[0]
        n_yaw = self.yaw_states.shape[0]
        n_ifl = self.ifl_states.shape[0]
        
        self.current_state = ifl_idx + n_ifl*yaw_idx + n_ifl*n_yaw*pit_idx + n_ifl*n_yaw*n_pit*aro_idx + n_ifl*n_yaw*n_pit*n_aro*val_idx

if __name__ == "__main__":
    def example_callback(action):
        print(action)
    mdp = BackchannelMDP(example_callback)
    
    print("TESTING _measurements_to_state()")
    measurement = np.array([[0.4, -0.6, 44, 1, 0, 4, 5, 4, 0]]).T
    mdp._measurements_to_state(measurement)
    print(f"Measurement (transposed):\t{measurement.T}")
    print(f"mdp.current_state (index):\t   {mdp.current_state}")
    print(f"State:\t\t\t\t {mdp.state_space[:, mdp.current_state]}")