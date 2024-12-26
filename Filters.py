# -*- coding: utf-8 -*-
"""
Filters
Average smoothing Gaussian Filter
Created on Sat Feb  8 18:31:24 2020
@author: Juan G. Diosa
ver 3.0
Improved Sat Mar 18 2023
"""

"""
###############################################################################
#Smoothing
Smooths the dot cloud height using averages 3x3

To Smooth the image, this script takes a sample of 3 x 3 from the main matrix.
Then, it calculates the average of the sample and replaces the pixel of the center
for the average. This scripts affects the pixels that are not in the
first and last rows or columns

  x x x 0 0 0 0 0             - - - 0 0 0 0 0
  x x x 0 0 0 0 0             - R - 0 0 0 0 0
  x x x 0 0 0 0 0             - - - 0 0 0 0 0
  0 0 0 0 0 0 0 0 -------->   0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0

  0 x x x 0 0 0 0             - - - 0 0 0 0 0
  0 x x x 0 0 0 0             - R R 0 0 0 0 0
  0 x x x 0 0 0 0             - - - 0 0 0 0 0
  0 0 0 0 0 0 0 0 -------->   0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0

  0 0 x x x 0 0 0             - - - - 0 0 0 0
  0 0 x x x 0 0 0             - R R R 0 0 0 0
  0 0 x x x 0 0 0             - - - - 0 0 0 0
  0 0 0 0 0 0 0 0 -------->   0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0             0 0 0 0 0 0 0 0

"""

def Smoothing(rows,columns,Dots):
    """
    # Input variables:
    # rows: an integer indicating the number of rows in the input array "Dots"
    # columns: an integer indicating the number of columns in the input array "Dots"
    # Dots: a 2D numpy array of shape (rows, columns) containing the input data
    
    # Output variable:
    # DotsMod: a 2D numpy array of the same shape as "Dots" containing the smoothed data
    """
      
      
    import numpy as np
    # Create an array of zeros with the same shape as the input array "Dots"
    DotsMod=np.zeros_like(Dots)
    
    # Fill the first and last rows of "DotsMod" with the corresponding rows from "Dots"
    DotsMod[0,:] = Dots[0,:]
    DotsMod[-1,:] = Dots[-1,:]
    
    # Fill the first and last columns of "DotsMod" with the corresponding columns from "Dots"
    DotsMod[:,0] = Dots[:,0]
    DotsMod[:,-1] = Dots[:,-1]
    
    # Create a 3x3 filter array with values 1/9
    filter = np.ones((3,3)) / 9
      
    # apply the filter to "Dots" using convolution
    import scipy.signal
    DotsMod[1:-1,1:-1] = scipy.signal.convolve2d(Dots, filter, mode='valid')
      
    return(DotsMod)

"""
##############################################################################
Gaussian
Smooth the dot cloud using a Gaussian filter in a matrix 5x5
##############################################################################
##############################################################################
Gaussian filter base on : https://www.youtube.com/watch?v=LZRiMS0hcX4&index=2&list=PLn6mvuS8j7h4fLrwY_AEfiYUUdhspffaz
##############################################################################

##############################################################################
------------------------------------------------------------------------------
This script generate a matrix to give weights to neighbour pixel to
influences the change of one pixel. Those weight are assign base on the
Gausssian distribution

G(x)=1/(sqrt(2*pi()*sigma*sigma))*exp(-1*(x^2+y^2)/(2*sigma*sigma))

For this case the only part that matter is the expoential term, because
the Matrix with the weights is going to be normalized.
To use this filter the matrix G must be odd and square, because the idea
is base on the distances to central pixel. x and y are position of the
pixel to the central one. Sigma is the standard deviation of the Gaussian
distribution.

In this case 5 x 5 matrix is used assuming sigma 1 we are going to have:

for the 1,1 place:

G(1,1)=exp(-1*(2^2+2^2)/2,) 2 is because it is two places way from the central position

After divide the whole matrix by the sum of all the elements, for this
case the Gaussian filter with the weights will look like:

         |1  4  7  4 1|
         |4 16 26 16 4|
  1/273  |7 26 41 26 7|
         |4 16 26 16 4|
         |1  4  7  4 1|
          
"""
#Filter
def Gaussian(sigma,rows,columns,Dots):
    """
    Input variables:
    
    sigma: the standard deviation of the Gaussian kernel used for the filter
    rows: the number of rows in the input image
    columns: the number of columns in the input image
    Dots: the input image as a 2D NumPy array
    Output variable:
    
    output: the filtered image as a 2D NumPy array

    """
    import numpy as np
    from scipy.signal import convolve2d
    # Create the Gaussian kernel
    x = np.arange(-2, 3)
    y = np.arange(-2, 3)
    xx, yy = np.meshgrid(x, y)
    kernel = np.exp(-(xx**2 + yy**2) / (2*sigma**2))
    kernel /= np.sum(kernel)
    
    """ 
    padarray creates a matrix with the info of one in the center and add
    x rows below and above, and y columns in both sides
    
                          0 0 0 0 0 0 0
                          0 0 0 0 0 0 0
        x x x             0 0 x x x 0 0
        x x x  -------->  0 0 x x x 0 0
        x x x             0 0 x x x 0 0
                          0 0 0 0 0 0 0
                          0 0 0 0 0 0 0
    """
  
  # Pad the input image with zeros
    Dots_pad = np.pad(Dots, ((2, 2), (2, 2)), mode='constant')
    """    
  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
  #-------------------------------------------------------------------------
  # A sample of 5 x 5 is taken from the original matrix, then this sample is
  # multiplied by the Gaussian matrix. Conv = A x G
  #
  #      A
  #   ----------
  #  |0 0 0 0 0|0 0 0
  #  |0 0 0 0 0|0 0 0
  #  |0 0 x x x|x 0 0          |0 0 0 0 0|         |1  4  7  4 1|
  #  |0 0 x x x|x 0 0          |0 0 0 0 0|         |4 16 26 16 4|
  #  |0 0 x x x|x 0 0    Conv= |0 0 x x x|   1/273 |7 26 41 26 7|
  #   ----------               |0 0 x x x|         |4 16 26 16 4|
  #   0 0 x x x x 0 0          |0 0 x x x|         |1  4  7  4 1|
  #   0 0 0 0 0 0 0 0
  #   0 0 0 0 0 0 0 0
  #
  # the sum of every single element of Conv will replace the central
  # element of the sample L=Sum of elements of Conv
  #
  #   ----------
  #  |0 0 0 0 0|0 0 0
  #  |0 0 0 0 0|0 0 0
  #  |0 0 x x x|x 0 0
  #  |0 0 x x x|x 0 0           L x x x
  #  |0 0 x x x|x 0 0           x x x x
  #   ----------      --------> x x x x
  #   0 0 x x x x 0 0           x x x x
  #   0 0 0 0 0 0 0 0
  #   0 0 0 0 0 0 0 0
  #
  #      ----------
  #   0 |0 0 0 0 0| 0 0
  #   0 |0 0 0 0 0| 0 0
  #   0 |0 x x x x| 0 0
  #   0 |0 x x x x| 0 0            L L x x
  #   0 |0 x x x x| 0 0            x x x x
  #      ----------      --------> x x x x
  #   0  0 x x x x 0 0             x x x x
  #   0  0 0 0 0 0 0 0
  #   0  0 0 0 0 0 0 0
  #
    """  
  # Apply the kernel to each pixel in the input image
    output = np.zeros((rows, columns))
    output = convolve2d(Dots, kernel, mode='same')
            
    return output
