# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 13:05:15 2023
@author: Juan
"""

###############################################################################
def DotsFromPicture(ImportedImage, height, TreatmentMod, sigma):
    # The function takes four input arguments: 
    # 1. ImportedImage: an image file that has been previously loaded in Python using the PIL module. 
    # 2. height: an integer representing the desired height of the output image.
    # 3. TreatmentMod: an integer that determines the type of filter to be applied. 
    # 4. sigma: a float representing the standard deviation of the Gaussian filter (if applicable).
    
    #------------------------------------------------------------------------------
    # Based on:
    # https://www.hackerearth.com/practice/notes/extracting-pixel-values-of-an-image-in-python/
    # the pixel information is read from the upper left corner, column by column.
    # then it continues with the second row and so on so forth
    
    import numpy as np
        
    # Get the dimensions of the input image    
    columns, rows = ImportedImage.size
    pixel = np.array(list(ImportedImage.getdata()))
    np.asarray(pixel)
    
    # Remove the alpha column information from the pixel array.
    pixel = pixel[:,:3]
    
    #--------------------------------------------------------------------------
    # Heights by colors
    # Matrix with heights base on a pixel scale
    from HeightsByColor import HeightsByColor
    Dots = HeightsByColor(height, columns, rows, pixel)
    
    #--------------------------------------------------------------------------
    # Smoothing or Gaussian filter and optional additional elements
    if TreatmentMod == 0:
      Dots = Dots      
    elif TreatmentMod == 1:
      from Filters import Smoothing     
      Dots = Smoothing(rows, columns, Dots)        
    else:
      from Filters import Gaussian 
      Dots = Gaussian(sigma, rows, columns, Dots)
      
    # Return the processed image matrix as well as the number of columns and rows of the original image.
    return(Dots, columns, rows)          
