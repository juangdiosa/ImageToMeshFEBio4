# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 08:44:17 2023
Define a function to calculate depths of skin layers base on levels, thickness and bias of each.
@author: Juandiosa
"""

def layersDepth(
        SCThickness, EpidermisLevels, EpidermisThickness, EpidermisBias, 
        DermisLevels, DermisThickness, DermisBias, 
        HypodermisLevels, HypodermisThickness, HypodermisBias):
    
    import numpy as np
    layerDepth = np.zeros((EpidermisLevels + DermisLevels + HypodermisLevels - 1, 1))
    
    #Viable Epidermis & Stratum Corneum
    layerDepth[1,0] = SCThickness
    
    # Stratum corneum just a layer. It is like shell 
    SCLevels = 1
    
    ViableEpidermisThickness = EpidermisThickness - SCThickness
    
    from Bias import BiasV
    EpidermisDepth = BiasV(EpidermisLevels, 
                           ViableEpidermisThickness, 
                           EpidermisBias)
    
    for capa in range(1, EpidermisLevels):        
        layerDepth[SCLevels + capa, 0] =  SCThickness + EpidermisDepth[capa,0]
    
        
    #Dermis
    DermisDepth = BiasV(DermisLevels, 
                        DermisThickness, 
                        DermisBias)
    
    #Epidermis levels includes SC
    for capa in range(1, DermisLevels):        
        layerDepth[EpidermisLevels + capa, 0] = EpidermisThickness + DermisDepth[capa,0]


    #Hypodermis
    HypodermisDepth = BiasV(HypodermisLevels, 
                        HypodermisThickness, 
                        HypodermisBias)
    
    for capa in range(1, HypodermisLevels):        
        layerDepth[EpidermisLevels + DermisLevels + capa -1, 0] = (EpidermisThickness 
                                                                   + DermisThickness 
                                                                   + HypodermisDepth[capa,0])

    return(layerDepth)


def layersDepthTension(
        SCThickness, EpidermisLevels, EpidermisThickness, EpidermisBias, 
        DermisLevels, DermisThickness, DermisBias):
    
    import numpy as np
    layerDepth = np.zeros((EpidermisLevels + DermisLevels - 1, 1))
    
    #Viable Epidermis & Stratum Corneum
    layerDepth[1,0] = SCThickness
    
    # Stratum corneum just a layer. It is like shell 
    SCLevels = 1
    
    ViableEpidermisThickness = EpidermisThickness - SCThickness
    
    from Bias import BiasV
    EpidermisDepth = BiasV(EpidermisLevels, 
                           ViableEpidermisThickness, 
                           EpidermisBias)
    
    for capa in range(1, EpidermisLevels):        
        layerDepth[SCLevels + capa, 0] =  SCThickness + EpidermisDepth[capa,0]
    
        
    #Dermis
    DermisDepth = BiasV(DermisLevels, 
                        DermisThickness, 
                        DermisBias)
    
    #Epidermis levels includes SC
    for capa in range(1, DermisLevels):        
        layerDepth[EpidermisLevels + capa -1, 0] = EpidermisThickness + DermisDepth[capa,0]

    return(layerDepth)