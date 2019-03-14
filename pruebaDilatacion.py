import numpy as np
import math

def dilatation(matrix, struct):
    neighbor = math.floor(int(len(struct))/2)
    rowO, columnO=matrix.shape
    row, column = struct.shape
    newImage = np.zeros((rowO,columnO))
    for i in range (neighbor,rowO-neighbor):
        for j in range (neighbor,columnO-neighbor):
            firsti = i - neighbor
            firstj = j - neighbor  
            endi = i + neighbor + 1
            endj = j + neighbor + 1
            #dilatation   
            # se esta suponiendo origen centro debo tener en cuenta opcion de centro 
            if ( matrix[i,j] == 1 ):
                newImage[firsti:endi,firstj:endj] = struct[:,:]
            else:
                newImage[firsti:endi,firstj:endj] = matrix[firsti:endi,firstj:endj]
    return newImage


m = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0., 1., 1., 1., 0., 0.],
       [0., 0., 1., 1., 1., 1., 0., 0., 0., 0., 1., 1., 1., 1., 0., 0.],
       [0., 0., 0., 1., 1., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
       [0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])

s = np.array([[1,1,1],[1,1,1],[1,1,1]])

print(dilatation(m,s))

