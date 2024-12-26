# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:49:16 2024
@author: Juan G. Diosa
Nodes Location In Layers gives the x, y, z coordinates in each mesh layer
"""

def NodesLocationInLayer(dx, dy, dots, Levels, 
                         NodesC, NodesX, NodesY, 
                         NodesZ, KLayermax, KLayermin, CountPos):    

    rows, columns = dots.shape
    
    for column in range(1, columns+1):
        for row in range(1, rows+1):
            for k in range(KLayermax,  KLayermin, -1):
              NodesC.append(CountPos)
              NodesX.append(dx * (column-1))
              NodesY.append(-dy * (row-1))
              NodesZ.append(Levels[k][row-1][column-1])
              CountPos += 1    
    return NodesC, NodesX, NodesY, NodesZ, CountPos 