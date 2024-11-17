import random
import threading
import wave
import time
import signal
import sys
from matplotlib import pyplot as plt

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
        #     M =   M4 = p1 (oldest)
        #           M5 = p2
        #           M6 = p3
        #           M7 = p4
        #           M8 = p5 (newest)
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
        self.pit_states = np.linspace(-1, 1, 5) # -35, 45
        self.yaw_states = np.linspace(-1, 1, 3) # -30, 30
        self.ifl_states = np.linspace(-1, 1, 3)
        grid = np.meshgrid(self.val_states, self.aro_states, self.pit_states, self.yaw_states, self.ifl_states, indexing='ij')
        self.state_space = np.reshape(grid, (5, -1))

        self.W = np.eye(5)
        self.W[2:, 2:] = 0
        self.utopia = np.array([[0, 0, 0, 0, 0]]).T
        
        # TODO: action_space is an array of the possible gestures and responses we can backchannel with
        self.action_space = np.array([["neutral",
                                      "thinking",
                                      "chatty",
                                      "exclaim",
                                      "inquire",
                                      "sigh",
                                      "lightbuilb",
                                      "affirmative_nod",
                                      "slow_nod",
                                      "curt_nod",
                                      "repetitive_nod",
                                      "horizontal_nod"]])
        
        self.action_space_mapping = np.array([[ 0.0,  0.0,  0.0,  0.0,  0.0],    # 0 Neutrual *
                                              [ 0.0,  0.5, -0.5,  1.0,  1.0],    # 1 Thinking *
                                              [ 0.5,  0.5,  0.5,  0.0,  1.0],    # 2 Chatty
                                              [ 0.5,  1.0,  1.0,  0.0,  1.0],    # 3 Exclaim *
                                              [ 0.0,  0.5,  0.5,  0.0,  1.0],    # 4 Inquire
                                              [-1.0,  0.5, -1.0,  0.0, -1.0],    # 5 Sad *
                                              [ 1.0,  0.5,  0.5,  0.0,  1.0],    # 6 Lightbulb *
                                              [ 0.5,  0.0,  0.0,  0.0,  0.0],    # 7 Affirm_nod *
                                              [ 0.0, -0.5,  0.0,  0.0,  1.0],    # 8 Slow_nod *
                                              [ 0.5,  0.5,  0.0,  0.0,  1.0],    # 9 Curt_nod
                                              [ 0.5,  1.0,  0.0,  0.0,  1.0],    # 10 Repetitive_nod *
                                              [-0.5, -0.5, -0.5, -1.0,  1.0]]).T # 11 Horizontal_nod *
        
        
        # current_state represents the column index of the current state in the context of state_space
        self.current_state = 0
        self.optimal_action = 0
        
        # MDP values
        self.action_space_size = self.action_space.shape[1]
        self.state_space_size = self.state_space.shape[1]
        
        # TODO: Make these work
        self.P = np.zeros((self.action_space_size, self.state_space_size, self.state_space_size))
        self.R = np.zeros((self.action_space_size, self.state_space_size, self.state_space_size))

        #self.P = np.random.rand(self.P.shape[0], self.P.shape[1], self.P.shape[2])
        #self.R = np.random.rand(self.R.shape[0], self.R.shape[1], self.R.shape[2])
        #self.P[:, :, 0] = 1
        #self.R[:, :, 0] = 1

        #self.P[self.P < 0.99] = 0
        #self.R[self.R < 0.99] = 0

        #self.P = self.P/np.sum(self.P, 2)[:, :, None]
       # self.R = self.R/np.sum(self.R, 2)[:, :, None]
        
        for action_idx in range(self.action_space_size):
            print(action_idx)
            for j in range(self.state_space_size):
                for k in range(self.state_space_size):
                    self.P[action_idx, j ,k] = self._calculate_transition(action_idx, self.state_space[:, j, None], self.state_space[:, k, None])
                    self.R[action_idx, j, k] = self._calculate_reward(action_idx, self.state_space[:, j, None], self.state_space[:, k, None])
        
        self.P = self.P-np.min(self.P, 2)[:, :, None]

        temp = np.sum(self.P, 2)
        idxs_i, idxs_j = np.where(temp < 0.000001)
        self.P[idxs_i, idxs_j, :] = 1
        self.P = self.P/np.sum(self.P, 2)[:, :, None]

        #self.R = np.random.rand(self.R.shape[0], self.R.shape[1], self.R.shape[2])
        #self.R[:, :, 0] = 1
        #self.R = self.R/np.sum(self.R, 2)[:, :, None]
        
        # random shit to make the code work
        self.callback = callback
        self.running = False
        
    def _run_helper(self):
        
        # take in measurements and convert to state
        #self._measurements_to_state(self.measurements)
        
        # Apply MDP to return optimal policy
        vi = mdp_tb.mdp.ValueIteration(self.P, self.R, 0.9, epsilon=0.1)
        vi.setVerbose()
        vi.run()

        # Apply optimal policy to current state to obtain optimal action
        self.optimal_action = vi.policy[self.current_state]

        while self.running:
            self._measurements_to_state(self.measurements)
            print(vi.policy)
            print(self.current_state)
            p = vi.policy[self.current_state]
            self.callback(self.action_space[0, p])
            self.running = False
        # TODO: Publish optimal action
        
        
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
        # ###########################################################################################
        self.measurements[2] = face_measurements[2]/40.0-0.125
        self.measurements[3] = face_measurements[3]/30.0
    
    # takes in speech measurements and applies them to self.measurements  
    def set_speech_measurements(self, speech_measurement):
        self.measurements[3:7] = self.measurements[4:8]
        self.measurements[8] = speech_measurement
        
    # given a set of possible bins, place x into the nearest bin and return that bin's index
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
        
        # If the fit is nearly linear, follow the linear slope instead
        if abs(quadratic_term) < 0.01:
            return 2 if linear_term > concavity_limit else (0 if linear_term < -concavity_limit else 1)
        
        if quadratic_term < -concavity_limit:
            ifl = 0 # Concave down
        elif -concavity_limit <= quadratic_term <= concavity_limit:
            ifl = 1 # Neutral
        else:
            ifl = 2 # Concave up
        return ifl
    
    # measurement is a column vector float of size 9
    # find closest state to given mesurements and then set current state to this index using self.state_space
    def _measurements_to_state(self, measurement):

        val_idx = self._quantize(measurement[0], self.val_states)
        aro_idx = self._quantize(measurement[1], self.aro_states)
        pit_idx = self._quantize(measurement[2], self.pit_states)
        yaw_idx = self._quantize(measurement[3], self.yaw_states)
        ifl_idx = self._get_inflection_idx(measurement[4:])
        
        n_aro = self.aro_states.shape[0]
        n_pit = self.pit_states.shape[0]
        n_yaw = self.yaw_states.shape[0]
        n_ifl = self.ifl_states.shape[0]
        
        self.current_state = ifl_idx + n_ifl*yaw_idx + n_ifl*n_yaw*pit_idx + n_ifl*n_yaw*n_pit*aro_idx + n_ifl*n_yaw*n_pit*n_aro*val_idx
        
    def _calculate_transition(self, action, initial_state, end_state):
        #probability = 0.0
        #print(action)
        action_characteristics = self.action_space_mapping[:,action, None] #pull a column of the action space mapping
        #print(end_state)
        #print(action_characteristics)
        #state_transition_magnitude = np.inner(initial_state, end_state)
        
        #probability += 1.0/state_transition_magnitude
        
        temp1 = initial_state+np.inner(initial_state, action_characteristics)*self.utopia
        probability = end_state[0, 0]*temp1[0, 0]+end_state[1, 0]*temp1[1, 0]
        #probability = end_state.T@self.W@(initial_state+(initial_state.T@action_characteristics)*self.utopia)
        
        
        # if states are close assign high probability
        # if states are far assign low probability
        #print(probability)
        #input()
        return probability
    
    def _calculate_reward(self, action, initial_state, end_state):
        reward = 0.0
        
        action_characteristics = self.action_space_mapping[:,action, None] #pull a column of the action space mapping
        
        
        
        # given changing conditions, add or subtract values from reward
        # increased valence --> good, more rewards
        
        reward = initial_state.T@action_characteristics
        return reward

if __name__ == "__main__":
    def example_callback(action):
        print(action)
    mdp = BackchannelMDP(example_callback)

    print("TESTING mdp._measurements_to_state()")
    measurement = np.array([[0.0, 0.5, 0.0, -45, 70, 60, 50, 40, 30]]).T
    mdp._measurements_to_state(measurement)
    print(f"Measurement:\t\t   {measurement.T}^T")
    print(f"mdp.current_state (index):    {mdp.current_state}")
    print(f"State:\t\t\t    {mdp.state_space[:, mdp.current_state]}")

    # This test will apply once the MDP has been implemented further
    mdp.start()
    time.sleep(90)
    mdp.stop()