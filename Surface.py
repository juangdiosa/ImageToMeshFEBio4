# -*- coding: utf-8 -*-
"""
Created on Sat Feb 08 16:00:31 2020
version:3.0
@author: Juan G. Diosa
Mod Thu June 20 2024
###############################################################################
#     UNIVERSIDAD DE ANTIOQUIA - PURDUE UNIVERSITY - UNIVERSIDAD CES          #
###############################################################################
#                  ***************************************                    #
#++++++                          Juan Diosa                             ++++++#
#                  ***************************************                    #
###############################################################################
# Use this source code is under CC BY-ND license, Any warranties are disclaimed.
###############################################################################

Creates a FEBio4 mesh for four skin layers from a png file or a sinusoidal 
surface given the amplitude and period.

"""
#------------------------------------------------------------------------------ 
# Time calculation of the script running
import timeit 
tic = timeit.default_timer()

#------------------------------------------------------------------------------ 
# Getting the file path to open
import os 
import glob
import pathlib

#https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
#answered by Aminius Feb 26 19 at 18:36
folder = str(pathlib.Path(__file__).parent.absolute())


############################################################################### 
# Surface dimensions 
#------------------------------------------------------------------------------ 
xDimension = 4 #<--------------------------------------------- Here X maximum value
yDimension = 4 #<--------------------------------------------- Here Y maximum value
height = 0.16#<------------------------------------------- Here Z maximun value

#------------------------------------------------------------------------------
# There are two treatments for the dot cloud :
# 1 Smoothing process using averages 3x3
# 2 Gaussian filter 5x5,a sigma value is required. 1 is used by default
TreatmentMod = 2; sigma = 0.75##<--------------------Write here the treatment option
# -------------------0 None, 1 to Smoothing, 2 to Gaussian and define sigma

# There are two options for the mesh:
# 0 Mesh WITHOUT addtional nodes to have a transtion from random height to zero
# 1 Mesh with addtional nodes to have a transtion from random height to zero
AdditionalNodesOption = 1
NumberOfAdditionalNodes = 3

# Additional nodes has two option [only 0 works with this script, 1 is for 
# a tension sample where only addional notes are needed in axial direction]
Sample = 0
# Surface options 
# There are two surface options :
# 1 Base on a picture
# 2 Sinusoidal
SurfaceOption = 1 #<--------------------------------------------- Here X maximum value

############################################################################### 
# Mesh
#---------------------------------------------------------------------------#
#Thickness of the layers

EpidermisThickness = 0.07
SCThickness = 0.02
DermisThickness = 0.84
HypodermisThickness = 2

#---------------------------------------------------------------------------#
#Number of levels and Bias for each one

EpidermisLevels = 3
EpidermisBias = 1.3
DermisLevels = 8
DermisBias = 1.3
HypodermisLevels = 6
HypodermisBias = 1.1

#%%

###############################################################################
#-----------------------------------------------------------------------------
# Define amplitude, frequency, square size, and meshgrid divisions
# If the sinusoidal surface is used, It is recommended not to use additional nodes
amplitude = 0.09
frequency = 6
squareSize = 4
divisions = 144

#------------------------------------------------------------------------------
# Png information and surface parameters
from PIL import Image
fileName = '7080Sq3000.png'                         #<-Write the Image Name here
filePath = folder+'/'+fileName
ImportedImage = Image.open(filePath, 'r')

#%%
###############################################################################
#------------------------------------------------------------------------------
# Surface options
if SurfaceOption == 1:
    from DotsFromPicture import DotsFromPicture
    Dots, columns, rows = DotsFromPicture(ImportedImage, height, TreatmentMod, sigma)
else:
    from SinusoidalSurface import SinusoidalSurface
    # Call the create_sinusoidal_surface function
    Dots, columns, rows = SinusoidalSurface(amplitude, frequency, squareSize, divisions)
    
#%%
#------------------------------------------------------------------------------
# Option additional elements
from AdditionalNodes import AdditionalNodes
if AdditionalNodesOption == 0:
    DotsMod = Dots
else:
    if SurfaceOption == 1:
        DotsMod = AdditionalNodes(Dots, NumberOfAdditionalNodes, Sample)
    else:
        from Filters import Smoothing
        DotsMod = Smoothing(divisions, 
                            divisions, 
                            AdditionalNodes(Dots, NumberOfAdditionalNodes, Sample))
#%%

###############################################################################
#------------------------------------------------------------------------------
# FEBIO Hexahedral mesh:
# Mesh with transition between rough to flat in the layers,
# multiplying the surface info by a percentage the skin surface

dy = yDimension/(rows-1)
dx = xDimension/(columns-1)

from MeshFeBioTransition import MeshFeBioTransition
MeshFeBioTransition(dx, dy, DotsMod,
                        EpidermisThickness, SCThickness, DermisThickness, HypodermisThickness,
                        EpidermisLevels, EpidermisBias,
                        DermisLevels, DermisBias, 
                        HypodermisLevels, HypodermisBias)

###############################################################################
#------------------------------------------------------------------------------ 
# Stop the time calculation of the script running
toc=timeit.default_timer()
T=(toc-tic)/60