# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 10:50:01 2023
@author: Juandiosa
"""
def NodesDepthInLayers(dots, layerDepth):
    import numpy as np
    # np.random.seed(8) 
    # dots = np.random.rand(2,3)
    
    rows, columns = dots.shape
    
    # layerDepth = np.array([[0], [0.02], [0.0417391], [0.07], [0.117774], [0.17988], [0.260618], [0.365577], [0.502024],
    # [0.679405], [0.91], [1.23759], [1.59795], [1.99434], [2.43037], [2.91]])
    
    # Calculate levels dynamically using a list
    levels = []
    
    levels.append(dots)  
    
    # Level 2 calculation: Subtract layerDepth[1,0] from all elements in the dots array
    level2 = dots - layerDepth[1, 0]    
    levels.append(level2)
      
    # Calculate levels 3 to 5 using list comprehension and vectorized operations
    multipliers = [0.75, 0.5, 0.25]  # Multipliers for levels 3, 4, 5
    for i in range(2, 5):
        level = multipliers[i - 2] * dots - layerDepth[i, 0]
        levels.append(level)
    
    # Levels 6 to 16: Fill the list with arrays of constant values multiplied by -1 * layerDepth
    for i in range(5, len(layerDepth)):
        level = -layerDepth[i, 0] * np.ones((rows, columns))
        levels.append(level)
    
    return(levels)