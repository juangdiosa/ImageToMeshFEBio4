# -*- coding: utf-8 -*-
"""
Mesh Febio Transition
Creates a mesh of five elements with a transition between rough surface to
flat for a Febio format
Created on Tue Feb 11 20:47:12 2020
@author: Juan G. Diosa
ver:3.0 on Thu June 20 2024 

The lowest cloud value must be 0 !!!!

"""
def MeshFeBioTransition(dx, dy, dots,
                        EpidermisThickness, SCThickness, DermisThickness, HypodermisThickness,
                        EpidermisLevels, EpidermisBias,
                        DermisLevels, DermisBias, 
                        HypodermisLevels, HypodermisBias):
                            
                            
    #############################################################################
    #Layers Depths
    #############################################################################    
    from LayersDepth import layersDepth
    layerDepth = layersDepth(
          SCThickness, EpidermisLevels, EpidermisThickness, EpidermisBias, 
          DermisLevels, DermisThickness, DermisBias,
          HypodermisLevels, HypodermisThickness, HypodermisBias)
    
    #############################################################################
    #Nodes Heights in each layer
    #############################################################################

    from NodesDepthInLayers import NodesDepthInLayers  
    Levels = NodesDepthInLayers(dots, layerDepth)

    #############################################################################
    #Nodes label and coordinates
    #############################################################################
    mesh = dict()
    from NodesLocation import NodesLocation
    mesh, NodesC = NodesLocation(mesh, dx, dy, dots, Levels, EpidermisLevels, 
                            DermisLevels, HypodermisLevels)

    #############################################################################
    #Elements
    #############################################################################

    from ElementsNodesConnectivity import ElementsNodesConnectivity
    rows, columns = dots.shape
    mesh = ElementsNodesConnectivity(rows, columns, EpidermisLevels, 
                                DermisLevels, HypodermisLevels,mesh)
      
    
    #############################################################################
    #FeBio Mesh File
    #############################################################################
    from FeBio4FileMultilayer import FeBioFile
    FeBioFile(mesh)
  