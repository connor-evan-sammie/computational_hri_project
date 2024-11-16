import numpy as np

action_space_mapping = np.array(             [[0.0, 0.0, 5.0, 0.0, 0.0],    # Neutrual
                                              [0.0, 0.5, -15.0, 30, 1.0],    # Thinking
                                              [0.5, 0.5, 25.0, 0.0, 1.0],    # Chatty
                                              [0.5, 1.0, 45.0, 0.0, 1.0],    # Exclaim
                                              [0.0, 0.5, 25.0, 0.0, 1.0],    # Inquire
                                              [-1.0, 0.5, -35, 0.0, -1.0],    # Sad
                                              [1.0, 0.5, 25.0, 0.0, 1.0],    # Lightbulb
                                              [0.5, 0, 5.0, 0.0, 0.0],    # Affirm_nod
                                              [0.0, -0.5, 5.0, 0.0, 1.0],    # Slow_nod
                                              [0.5, 0.5, 5.0, 0.0, 1.0],    # Curt_nod
                                              [0.5, 1.0, 5.0, 0.0, 1.0]]).T

print(action_space_mapping)