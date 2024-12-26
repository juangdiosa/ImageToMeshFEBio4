# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 12:16:27 2023
@author: Juan G Diosa
"""

def SinusoidalSurface(amplitude, frequency, square_size, divisions):
    """
    Creates a 3D sinusoidal surface using the specified amplitude, frequency, and size of the square.
    
    Args:
        amplitude (float): The amplitude of the wave.
        frequency (float): The frequency of the wave.
        square_size (float): The size of the square in which the surface is defined.
        divisions (int): The number of divisions in the X and Y dimensions of the surface grid.
    
    Returns:
        tuple: A tuple containing the X, Y, and Z arrays representing the grid of points on the surface,
        with the specified number of divisions in each dimension.
    """
    
    import numpy as np
    
    # Create a grid of x and y values with the specified divisions
    x = np.linspace(-square_size/2, square_size/2, divisions)
    y = np.linspace(-square_size/2, square_size/2, divisions)
    X, Y = np.meshgrid(x, y)
    
    # Compute z values using the formula for a sinusoidal wave
    Z = amplitude * np.sin(2*np.pi*frequency*(X/square_size)) * np.sin(2*np.pi*frequency*(Y/square_size))
    
    Z = Z+abs(np.min(Z)) * np.ones((divisions, divisions))
    
    # Return the X divisions , Y divisions, and Z arrays    
    return (Z, divisions, divisions)