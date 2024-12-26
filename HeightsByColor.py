# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:24:16 2020
Matrix of Image
Creates a matrix with the color info of each pixel of a picture
@author: Juan G. Diosa
Improved Sat Mar 18 2023
"""

def HeightsByColor(height, columns, rows, Image):
    """
    
    
    Input:
    
    height: a float representing the maximum height value of the terrain
    columns: an integer representing the number of columns in the image
    rows: an integer representing the number of rows in the image
    Image: a 3D numpy array representing the color image
    Output:
    
    height_array: a 2D numpy array representing the height values for each color in 
    the input image, where the dimensions of the array are (rows, columns)

    """
    import numpy as np
      # Reshape the 3D image array into a 2D array with 3 columns
    Image_2d = Image.reshape(columns * rows, 3)

    # Find the unique colors in the image and assign them a height value
    unique_colors, color_indices = np.unique(Image_2d, axis=0, return_inverse=True)
    height_values = np.linspace(0, height, num=len(unique_colors), endpoint=True)
    height_array = height_values[color_indices].reshape(rows, columns)
    
    return height_array