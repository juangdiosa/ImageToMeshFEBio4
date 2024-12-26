# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:54:29 2024

@author: Juan G Diosa 
Nodes Location stores in a dictionary the nodes and elements information
"""

def NodesLocation(mesh, dx, dy, dots, Levels, EpidermisLevels, 
                  DermisLevels, HypodermisLevels):
    if not bool(mesh):
        CountPos = 1
    else:
        CountPost = len(mesh['Nc'])+1
    
    import numpy as np
    
    NodesC=[]
    NodesX=[]
    NodesY=[]
    NodesZ=[]

    
    rows, columns = dots.shape
    
    #stratum corneum layers = 2
    StratumLayers=2
    KLayermax =  StratumLayers-1
    KLayermin = -1
    from NodesLocationInLayer import NodesLocationInLayer
    
    NodesC, NodesX, NodesY, NodesZ, CountPos = NodesLocationInLayer(dx, dy, dots, Levels, 
                             NodesC, NodesX, NodesY, 
                             NodesZ, KLayermax, KLayermin, CountPos)
    
    mesh['Nc'] = NodesC[0::]
    mesh['Nx'] = NodesX[0::]
    mesh['Ny'] = NodesY[0::]
    mesh['Nz'] = NodesZ[0::]
        
    #Viable epidermis   
    KLayermax = EpidermisLevels
    KLayermin = StratumLayers-1
    
    NodesC, NodesX, NodesY, NodesZ, CountPos = NodesLocationInLayer(dx, dy, dots, Levels, 
                             NodesC, NodesX, NodesY, 
                             NodesZ, KLayermax, KLayermin, CountPos)
    
    mesh['Nc2'] = NodesC[len(mesh['Nc'])::]
    mesh['Nx2'] = NodesX[len(mesh['Nc'])::]
    mesh['Ny2'] = NodesY[len(mesh['Nc'])::]
    mesh['Nz2'] = NodesZ[len(mesh['Nc'])::]
    
    #Dermis 
    KLayermax = EpidermisLevels+DermisLevels-1
    KLayermin = EpidermisLevels
    
    NodesC, NodesX, NodesY, NodesZ, CountPos = NodesLocationInLayer(dx, dy, dots, Levels, 
                             NodesC, NodesX, NodesY, 
                             NodesZ, KLayermax, KLayermin, CountPos)
    
    mesh['Nc3'] = NodesC[len(mesh['Nc'])+len(mesh['Nc2'])::]
    mesh['Nx3'] = NodesX[len(mesh['Nc'])+len(mesh['Nc2'])::]
    mesh['Ny3'] = NodesY[len(mesh['Nc'])+len(mesh['Nc2'])::]
    mesh['Nz3'] = NodesZ[len(mesh['Nc'])+len(mesh['Nc2'])::]
       
    #Hypodermis
    KLayermax = EpidermisLevels+DermisLevels+HypodermisLevels-2
    KLayermin = EpidermisLevels+DermisLevels-1
    
    NodesC, NodesX, NodesY, NodesZ, CountPos = NodesLocationInLayer(dx, dy, dots, Levels, 
                             NodesC, NodesX, NodesY, 
                             NodesZ, KLayermax, KLayermin, CountPos)    

    mesh['Nc4'] = NodesC[len(mesh['Nc'])+len(mesh['Nc2'])+len(mesh['Nc3'])::]
    mesh['Nx4'] = NodesX[len(mesh['Nc'])+len(mesh['Nc2'])+len(mesh['Nc3'])::]
    mesh['Ny4'] = NodesY[len(mesh['Nc'])+len(mesh['Nc2'])+len(mesh['Nc3'])::]
    mesh['Nz4'] = NodesZ[len(mesh['Nc'])+len(mesh['Nc2'])+len(mesh['Nc3'])::]
   
    return mesh, NodesC

mesh = dict()
dx = 0.1
dy = 0.1
import numpy as np

#np.random.seed(13) 

#dots = np.random.rand(3,2)
dots = np.load('DotsMod.npy')
#Levels = (0, 0.02, 0.0417391, 0.07, 0.117774, 0.17988, 0.260618, 0.365577, 0.502024,
#                       0.679405, 0.91, 1.23759, 1.59795, 1.99434, 2.43037, 2.91)
Levels = np.array([[0], [0.02], [0.0417391], [0.07], [0.117774], [0.17988], [0.260618], [0.365577], [0.502024],
                       [0.679405], [0.91], [1.23759], [1.59795], [1.99434], [2.43037], [2.91]])

EpidermisLevels = 3
DermisLevels = 8
HypodermisLevels = 6

mesh, NodesC = NodesLocation(mesh, dx, dy, dots, Levels, EpidermisLevels, 
                  DermisLevels, HypodermisLevels)