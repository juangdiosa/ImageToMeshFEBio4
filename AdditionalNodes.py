# -*- coding: utf-8 -*-
"""
AdditionalDots
Created on Sat Feb  8 20:40:35 2020
Created new rows and columns in order to avoid the boundary conditions influences
@author: Juan G. Diosa
Ver:2.0
Improved Sat Mar 18 2023
"""
def AdditionalNodes(dots, NumberOfAdditionalNodes, Sample):
    import numpy as np
    # Additional nodes has two option for sample
    # 0 works with this script surface from Mesh from Image, 
    # 1 is for this case a tension sample
    rows = dots.shape[0]
    
    """
     A=additional
               
               |        --> Columns <--  
               V          |         |
                    0 0 0 0 0 0 0 0 0 0 0 0    |  
               A    0 0 0 0 0 0 0 0 0 0 0 0    |
                    0 0 0 0 0 0 0 0 0 0 0 0 ---V
               ^    0 0 0 x x x x x x 0 0 0   
               |    0 0 0 x x x x x x 0 0 0    R  
                    0 0 0 x x x x x x 0 0 0    o 
               |    0 0 0 x x x x x x 0 0 0    w  
               V    0 0 0 x x x x x x 0 0 0
                    0 0 0 0 0 0 0 0 0 0 0 0 ---^           
               A    0 0 0 0 0 0 0 0 0 0 0 0    | 
                    0 0 0 0 0 0 0 0 0 0 0 0    | 
               ^  -->  A  <--      -->  A  <--
               | 
    """
    
    BigMatrixZ = np.pad(dots,
                        pad_width = NumberOfAdditionalNodes,
                        mode = 'constant',
                        constant_values = 0)
    
    """
    Getting information from first, second, penultimate and last column with
    skin topography information
    Acolumn=a
    Bcolumn=b
    Acolumns=A
    Bcolumns=B
                        0 0 0 0 0 0 0 0 0 0 0 0
                        0 0 0 0 0 0 0 0 0 0 0 0
                        0 0 0 0 0 0 0 0 0 0 0 0
                        0 0 0 a b x x A B 0 0 0
                        0 0 0 a b x x A B 0 0 0
                        0 0 0 a b x x A B 0 0 0
                        0 0 0 a b x x A B 0 0 0
                        0 0 0 a b x x A B 0 0 0
                        0 0 0 0 0 0 0 0 0 0 0 0
                        0 0 0 0 0 0 0 0 0 0 0 0
                        0 0 0 0 0 0 0 0 0 0 0 0
    
    """
    
    Acolumn = dots[:,0]
    Bcolumn = dots[:,-1]
    
    Acolumns = dots[:,1]
    Bcolumns = dots[:,-2]
 
    #-------------------------------------------------------------------------%
    # SHAPE FOR THE ADDITIONAL COLUMNS  
    # To avoid possible issues with edges in the mesh, two different shape are
    # used. Base on the slope the script chooses between S shape and parabola. 
    
    for i in range(NumberOfAdditionalNodes + 1, NumberOfAdditionalNodes + rows + 1):
      #S Shape if the slope between the first and the second columns is
      #negative 
      if Acolumn[i - NumberOfAdditionalNodes - 1] > Acolumns[ i - NumberOfAdditionalNodes - 1]:
        
        for k in range(1, 2+int(NumberOfAdditionalNodes/2)):
          pa = ((1+ NumberOfAdditionalNodes/2)**2)/(4 * Acolumn[i-NumberOfAdditionalNodes-1]/2)
          BigMatrixZ[i-1,k-1] = (k**2) / (4*pa)
          
        for k in range(1+int(NumberOfAdditionalNodes/2), NumberOfAdditionalNodes+1):
          pa = ((1+ NumberOfAdditionalNodes/2)**2)/(4*Acolumn[i-NumberOfAdditionalNodes-1]/2)
          BigMatrixZ[i-1,k-1] = -((NumberOfAdditionalNodes+1-k)**2)/(4*pa)+Acolumn[i-NumberOfAdditionalNodes-1]
      #S Shape if the slope between the penultimate and the last columns is
      #positive
          
      if Bcolumn[i-NumberOfAdditionalNodes-1] > Bcolumns[i-NumberOfAdditionalNodes-1]:
        
        for k in range(1,2+int(NumberOfAdditionalNodes/2)):
          pb = ((NumberOfAdditionalNodes/2)**2)/(4*Bcolumn[i-NumberOfAdditionalNodes-1]/2)
          BigMatrixZ[i-1,-k] = (k**2)/(4*pb)
         
        for k in range(1+int(NumberOfAdditionalNodes/2),NumberOfAdditionalNodes+1):
          pb = ((1+NumberOfAdditionalNodes/2)**2)/(4*Bcolumn[i-NumberOfAdditionalNodes-1]/2)
          BigMatrixZ[i-1,-k] = -((NumberOfAdditionalNodes+1-k)**2)/(4*pb) + Bcolumn[i-NumberOfAdditionalNodes-1]
          
      #Parabola Shape if the slope between the first and the second columns is
      #positive
      if Acolumn[i-NumberOfAdditionalNodes-1] < Acolumns[i-NumberOfAdditionalNodes-1]:
        
        for k in range(1, NumberOfAdditionalNodes+2):
          pa = (NumberOfAdditionalNodes**2) / (4*Acolumn[i-NumberOfAdditionalNodes-1])
          BigMatrixZ[i-1,k-1] = (k**2) / (4*pa)
    
      if Bcolumn[i-NumberOfAdditionalNodes-1] < Bcolumns[i-NumberOfAdditionalNodes-1]:
        
        for k in range(1,NumberOfAdditionalNodes+2):
          pb = (NumberOfAdditionalNodes**2) / (4*Bcolumn[i-NumberOfAdditionalNodes-1])
          BigMatrixZ[i-1,-k] = (k**2)/(4*pb)
    
    
    if Sample == 0:
        
        """
        For sample with a general purpose 
        Getting information from first, second, penultimate and last row from the
        new matrix generated in the last step
        Arow=a
        Brow=b
        Arows=A
        Brows=B
                            0 0 0 0 0 0 0 0 0 0 0 0
                            0 0 0 0 0 0 0 0 0 0 0 0
                            0 0 0 0 0 0 0 0 0 0 0 0
                            a a a a a a a a a a a a
                            b b b b b b b b b b b b
                            x x x x x x x x x x x x
                            B B B B B B B B B B B B
                            A A A A A A A A A A A A
                            0 0 0 0 0 0 0 0 0 0 0 0
                            0 0 0 0 0 0 0 0 0 0 0 0
                            0 0 0 0 0 0 0 0 0 0 0 0
        
        
        """
        
        columnsBig = BigMatrixZ.shape[1]    
        Arow = BigMatrixZ[NumberOfAdditionalNodes, :]
        Brow = BigMatrixZ[-1-NumberOfAdditionalNodes, :]
        
        Arows = BigMatrixZ[NumberOfAdditionalNodes+1, :]
        Brows = BigMatrixZ[-2-NumberOfAdditionalNodes, :]
        
        #-------------------------------------------------------------------------# 
    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
        #-------------------------------------------------------------------------#
        # SHAPE FOR THE ADDITIONAL ROWS
        # Here the same strategy used for the columns was applied   
        for S in range(1, columnsBig+1):
        #S Shape if the slope between the first and the second row is
        #negative
          if Arow[S-1] > Arows[S-1]:
            for k in range(1, NumberOfAdditionalNodes+2):
                pa = ((1+NumberOfAdditionalNodes/2)**2) / (4*Arow[S-1]/2)
                BigMatrixZ[k-1,S-1] = (k**2) / (4*pa)
            
            for k in range(int(1+NumberOfAdditionalNodes/2), NumberOfAdditionalNodes+2):
                pa = ((1+NumberOfAdditionalNodes/2)**2) / (4*Arow[S-1]/2)
                BigMatrixZ[k-1,S-1] = -((NumberOfAdditionalNodes+1-k)**2) / (4*pa)+Arow[S-1]
                
          #S Shape if the slope between the penultimate and the last row is
          #positive
          if Brow[S-1] > Brows[S-1]:
            for k in range(1, NumberOfAdditionalNodes+2):
                pb=((1+NumberOfAdditionalNodes/2)**2) / (4*Brow[S-1]/2)
                BigMatrixZ[-k,S-1] = (k**2) / (4*pb)
            
            for k in range(1+int(NumberOfAdditionalNodes/2), NumberOfAdditionalNodes+2):
                pb=((1+NumberOfAdditionalNodes/2)**2) / (4*Brow[S-1]/2)
                BigMatrixZ[-k,S-1] = -((NumberOfAdditionalNodes+1-k)**2) / (4*pb)+Arow[S-1]
          #Parabola Shape if the slope between the first and the second row is
          #positive
          if Arow[S-1] < Arows[S-1]:
            for k in range(1, NumberOfAdditionalNodes+2):
              pa = (NumberOfAdditionalNodes**2) / (4*Arow[S-1])
              BigMatrixZ[k-1,S-1] = (k**2)/(4*pa)
          #Parabola Shape if the slope between the penultimate and the last row is
          #Negative
          if Brow[S-1] < Brows[S-1]:
            for k in range(1, NumberOfAdditionalNodes+2):
              pb = (NumberOfAdditionalNodes**2) / (4*Brow[S-1])
              BigMatrixZ[-k,S-1] = (k**2)/(4*pb)
    
        #-------------------------------------------------------------------------# 
    
        #-------------------------------------------------------------------------#
        # ADDITIONAL ROW AND COLUMNS WITH 0 HEIGHT 
        # new big matrix of zeros is generated and the matrix with the information of skin
        # and the treated edges is placed in the center
        #
        #           |        --> Columns <--  
        #           V          |         |
        #                0 0 0 0 0 0 0 0 0 0 0 0    |  
        #           A    0 0 0 0 0 0 0 0 0 0 0 0    |
        #                0 0 0 0 0 0 0 0 0 0 0 0 ---V
        #           ^    0 0 0 x x x x x x 0 0 0   
        #           |    0 0 0 x x x x x x 0 0 0    R  
        #                0 0 0 x x x x x x 0 0 0    o 
        #           |    0 0 0 x x x x x x 0 0 0    w  
        #           V    0 0 0 x x x x x x 0 0 0
        #                0 0 0 0 0 0 0 0 0 0 0 0 ---^           
        #           A    0 0 0 0 0 0 0 0 0 0 0 0    | 
        #                0 0 0 0 0 0 0 0 0 0 0 0    | 
        #           ^  -->  A  <--      -->  A  <--
        #           | 
        #
        divisions = 2
        BiggerMatrixZ = np.pad(BigMatrixZ,
                               pad_width = divisions,
                               mode='constant',
                               constant_values = 0)
        return(BiggerMatrixZ)
    else:
        # For a tension sample
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
        #-------------------------------------------------------------------------#
        #      
        #                    0 0 0 0 0 0 0 0 0 0 0 0
        #                    0 0 0 0 0 0 0 0 0 0 0 0
        #                    0 0 0 0 0 0 0 0 0 0 0 0
        #                    a a a a a a a a a a a a
        #                    b b b b b b b b b b b b
        #                    x x x x x x x x x x x x
        #                    B B B B B B B B B B B B
        #                    A A A A A A A A A A A A
        #                    0 0 0 0 0 0 0 0 0 0 0 0
        #                    0 0 0 0 0 0 0 0 0 0 0 0
        #                    0 0 0 0 0 0 0 0 0 0 0 0
        #
        #                               |
        #                               |
        #                               |
        #                               v
        #
        #                    a a a a a a a a a a a a
        #                    b b b b b b b b b b b b
        #                    x x x x x x x x x x x x
        #                    B B B B B B B B B B B B
        #
        #     
        BigMatrixZ = BigMatrixZ[NumberOfAdditionalNodes:NumberOfAdditionalNodes+dots.shape[0],:]
    
        #-------------------------------------------------------------------------#
        # ADDITIONAL COLUMNS WITH 0 HEIGHT 
        # new big matrix of zeros is generated and the matrix with the information of skin
        # and the treated edges is placed in the center
        #
        #                    --> Columns <--  
        #                      |         |
        #                0 0 0 x x x x x x 0 0 0   
        #                0 0 0 x x x x x x 0 0 0      
        #                0 0 0 x x x x x x 0 0 0     
        #                0 0 0 x x x x x x 0 0 0  
        #                0 0 0 x x x x x x 0 0 0
        #              -->  A  <--      -->  A  <--
        #
        divisions=2
        BiggerMatrixZ = np.pad(BigMatrixZ,
                               ((0,0),(divisions,divisions)),
                               mode='constant',
                               constant_values=0)
            
        return(BiggerMatrixZ)