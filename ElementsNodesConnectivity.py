# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 09:29:01 2024
@author: Juan Diosa
"""

def ElementsNodesConnectivity(rows, columns, EpidermisLevels, DermisLevels, HypodermisLevels, mesh):
    import numpy as np
    #Elements
    #Coordinate system Z is normal to the screen
    #This code creates the conectivity for each skin layer, it begins from the
    #upper left corner in the deepest level for each skin layer
    #(starting stratum, viable epidermis, .....,Hypodermis). The following
    #nodes are wich are above (from deeper to closest to the surface) until
    #reach the outer level of that skin layer. the CountPosing increses from the
    #first row to the last and continue to the next column.
    #-------------------------------------------------------------------------#
    #Stratum Corneum Elements
    Ec = []
    E1 = []
    E2 = []
    E3 = []
    E4 = []
    E5 = []
    E6 = []
    E7 = []
    E8 = []
    CountPos = 1
   
    # THIS PART IS VALID FOR STRATUM CORNEUM ONLY !!!!!
    #Ec has the node label base on count
    #E5: 2*i-1+ rows * 2 * (j-1);
    # (2*i-1) is the row term,It begins from deeper layer and gives a label for
    # each node of the matrix. 2 is the number of layers of stratum corneum,
    # i the row, and -1 helps to continue being in the deeper layer.
    # (rows*2*(j-1)) is the column term, where 2 it is the number of layer of
    # stratum corneum, and with rows help to give the proper label in each
    # column. (j-1) is a swith.
    #E6 is in the same row of E5 but in the next column = E5 + Rows * 2, where 2 is the number of layers
    #E7 is above of E7: E6 + 2, where 2 is the number of layers
    #E8 is above of E5: E5 + 2, where 2 is the number of layers
    #E1,E2,E3 and E4 are in the next row of E5,E6,E7 and E8 respectibily
    
    for j in range(1, columns):
        for i in range(1, rows):
            Ec.append(CountPos)
            E5.append(2 * i-1+rows * 2 * (j-1))
            E6.append(E5[CountPos-1]+2 * rows)
            E7.append(E6[CountPos-1]+2)
            E8.append(E5[CountPos-1]+2)
            E1.append(E5[CountPos-1]+1)
            E2.append(E6[CountPos-1]+1)
            E3.append(E7[CountPos-1]+1)
            E4.append(E8[CountPos-1]+1)
            CountPos += 1
    
    mesh['Ec']=Ec
    mesh['E1']=E1
    mesh['E2']=E2
    mesh['E3']=E3
    mesh['E4']=E4
    mesh['E5']=E5
    mesh['E6']=E6
    mesh['E7']=E7
    mesh['E8']=E8
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    # STRATEGY OF VIABLE EPIDERMIS, DERMIS AND HYPODERMIS
    #Ec has the node label acording to the general counting
    #E5: [(PreviousLayers)*rows*colum]+[(#LevelsOfLayers-1)*i-(#LevelsOfLayers-2)]
    # +(k-1)+[(#LevelsOfLayers-1)*rows*(j-1)];
    #(~) [(PreviousLayers)*rows*colum], It gives initial number of node for each
    # layers
    #(~) [(#LevelsOfLayers-1)*i-(#LevelsOfLayers-2)] is the row term,
    # It begins from deeper layer and gives a label for each node of the matrix.
    # where i is the row parameter of for loop
    #(~)(k-1) is the element deep term, k is the deep parameter of for loop
    # and It is number of levels of layers minus 1
    #(~)[(#LevelsOfLayers-1)*rows*(j-1)] is the column term, (j-1) is a swith
    # where j is the column parameter of for loop
    #E6 is in the same row of E5 but in the next column = E5 + Rows * N, where
    #N is the number of levels minus 1
    #E7 is above of E6: E6 + N, N is the number of levels
    #E8 is above of E5: E5 + N, N is the number of levels
    # If k=(#LevelsOfLayers-1) E1,E2,E3 and E4 are E5 (without (k-1)term), E6,
    # E7 and E8 of previous layers, otherwise
    #E1,E2,E3 and E4 are in the next row of E5,E6,E7 and E8 respectibily (E1=E5+1)
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    #-------------------------------------------------------------------------#
    #Viable Epidermis
    Ec2 = []
    E12 = []
    E22 = []
    E32 = []
    E42 = []
    E52 = []
    E62 = []
    E72 = []
    E82 = []
    position = 1
    for j in range(1, columns):
        for i in range(1, rows):
            for k in range(1, EpidermisLevels):
                Ec2.append(CountPos)
                E52.append(2 * rows * columns+(EpidermisLevels-1) * i-(EpidermisLevels-2)+(k-1)+(EpidermisLevels-1) * rows * (j-1))
                E62.append(E52[position-1]+(EpidermisLevels-1) * rows)
                E72.append(E62[position-1]+2)
                E82.append(E52[position-1]+2)
                if k == EpidermisLevels-1:
                    E12.append(2 * i-1+rows * 2 *(j-1))
                    E22.append(E12[position-1]+2 * rows)
                    E32.append(E22[position-1]+2)
                    E42.append(E12[position-1]+2)
                else:
                    E12.append(E52[position-1]+1)
                    E22.append(E62[position-1]+1)
                    E32.append(E72[position-1]+1)
                    E42.append(E82[position-1]+1)
                CountPos += 1
                position += 1
     
    mesh['Ec2']=Ec2
    mesh['E12']=E12
    mesh['E22']=E22
    mesh['E32']=E32
    mesh['E42']=E42
    mesh['E52']=E52
    mesh['E62']=E62
    mesh['E72']=E72
    mesh['E82']=E82
    #-------------------------------------------------------------------------#
    #Dermis
    Ec3 = []
    E13 = []
    E23 = []
    E33 = []
    E43 = []
    E53 = []
    E63 = []
    E73 = []
    E83 = []
    position = 1
    for j in range(1, columns):
        for i in range(1, rows):
            for k in range(1, DermisLevels):
                Ec3.append(CountPos)
                E53.append((2+EpidermisLevels-1) * rows * columns+(DermisLevels-1) * i-(DermisLevels-2)+(k-1)+(DermisLevels-1) * rows * (j-1))
                E63.append(E53[position-1]+(DermisLevels-1) * rows)
                E73.append(E63[position-1]+(DermisLevels-1))
                E83.append(E53[position-1]+(DermisLevels-1))
                if k == DermisLevels-1:
                    E13.append(2 * rows * columns+(EpidermisLevels-1) * i-(EpidermisLevels-2)+(EpidermisLevels-1) * rows * (j-1))
                    E23.append(E13[position-1]+(EpidermisLevels-1) * rows)
                    E33.append(E23[position-1]+(EpidermisLevels-1))
                    E43.append(E13[position-1]+(EpidermisLevels-1))
                else:
                    E13.append(E53[position-1]+1)
                    E23.append(E63[position-1]+1)
                    E33.append(E73[position-1]+1)
                    E43.append(E83[position-1]+1)
                CountPos += 1
                position += 1
            
    mesh['Ec3']=Ec3
    mesh['E13']=E13
    mesh['E23']=E23
    mesh['E33']=E33
    mesh['E43']=E43
    mesh['E53']=E53
    mesh['E63']=E63
    mesh['E73']=E73
    mesh['E83']=E83
    
    #-------------------------------------------------------------------------#
    #Hypodermis
    Ec4 = []
    E14 = []
    E24 = []
    E34 = []
    E44 = []
    E54 = []
    E64 = []
    E74 = []
    E84 = []
    position = 1
    for j in range(1, columns):
        for i in range(1, rows):
            for k in range(1, HypodermisLevels):
                Ec4.append(CountPos)
                E54.append((2+EpidermisLevels-1+DermisLevels-1) * rows * columns+(HypodermisLevels-1) * i-(HypodermisLevels-2)+(k-1)+(HypodermisLevels-1) * rows * (j-1))
                E64.append(E54[position-1]+(HypodermisLevels-1) * rows)
                E74.append(E64[position-1]+(HypodermisLevels-1))
                E84.append(E54[position-1]+(HypodermisLevels-1))
                if k == HypodermisLevels-1:
                    E14.append((2+EpidermisLevels-1) * rows * columns+(DermisLevels-1) * i-(DermisLevels-2)+(DermisLevels-1) * rows * (j-1))
                    E24.append(E14[position-1]+(DermisLevels-1) * rows)
                    E34.append(E24[position-1]+(DermisLevels-1))
                    E44.append(E14[position-1]+(DermisLevels-1))
                else:
                    E14.append(E54[position-1]+1)
                    E24.append(E64[position-1]+1)
                    E34.append(E74[position-1]+1)
                    E44.append(E84[position-1]+1)
                CountPos += 1
                position += 1    
     
    mesh['Ec4']=Ec4
    mesh['E14']=E14
    mesh['E24']=E24
    mesh['E34']=E34
    mesh['E44']=E44
    mesh['E54']=E54
    mesh['E64']=E64
    mesh['E74']=E74
    mesh['E84']=E84
    
    return mesh