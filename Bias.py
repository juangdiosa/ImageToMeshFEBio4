# -*- coding: utf-8 -*-
"""
Bias
Created on Wed Feb 12 07:17:20 2020
Return distance between layers
@author: Juan G Diosa

This function calculates the distance between layers in a multilayer 
structure, given the number of layers, the thickness of the structure, 
and a bias factor.
Improved Sat Mar 18 2023
"""
def BiasV(layers,thickness,bias):
    import numpy as np
    
    #-------------------------------------------------------------------------#
    # Create an array of zeros to store the distances between layers.
    dz=np.zeros((layers,1))
    
    # Bias factor is equal to 1.
    if bias==1:
        # If it is, the distance between each layer is the same, and the function calculates 
        # the distance using the formula (thickness/(layers-1)).
        for m in range(2,layers+1):
            dz[m-1,0]=dz[m-2,0]+(thickness/(layers-1))
            
    else:
        # If the bias factor is not equal to 1, the function uses a different 
        # formula to calculate the distance between layers.
        # The formula takes into account the bias factor and ensures 
        # that the distance between layers changes exponentially from one layer to the next.
        
        
        # Calculate the sum of the geometric series (bias^0 + bias^1 + ... + bias^(layers-2)).
        bfac=0
        for a in range(1,layers):
            bfac=bfac+bias**(a-1)
            
        # Calculate the distance between the layers based on the bias 
        # factor and the total thickness of the structure.
        zbias=thickness/bfac
        dz[1,0]=dz[0,0]+zbias
        for e in range(3,layers):
            dz[e-1,0]=dz[e-2,0]+(zbias*bias**(e-2))
        dz[layers-1,0]=thickness
        
    # Return the array of distances between layers.   
    return(dz)