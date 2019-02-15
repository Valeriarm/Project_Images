import numpy as np
import copy
import math
from matplotlib import pyplot as plt
from skimage import io

dicomImage = []

VALUES = 65536
NEIGHBORS = 1      

def histogram(matrix):
    row, column = matrix.shape
    hist = [0]*VALUES
    for i in range (0,column-1):
        for j in range(0,row-1):
            index = matrix[i][j]
            hist[index]+=1
    return hist

def applyConvolution(original,kernel,borderline):
    #kernel = getKernel(kernelName)
    NEIGHBORS = int((len(kernel)/2)-0.5)
    #print(str(isinstance(NEIGHBORS,int)))
    #definir la cantidad de vecinos respecto al kernel escogido
    rowO, columnO=original.shape
    #print("row"+str(rowO)+"\ncolumn"+str(columnO)+str(NEIGHBORS))
    #adiciona fila o columna a cada extremo y copia su valor correspondiente.
    image = original
    if ( borderline == 'reflejados'):
        image = np.pad(original,NEIGHBORS,'symmetric')
    elif ( borderline == 'ceros') :
        image = np.pad(original,NEIGHBORS, 'constant', constant_values=(0))
    row, column = image.shape
    #nueva imagen
    newImage = np.zeros((rowO,columnO))
    m = 0
    n = 0
    for i in range (NEIGHBORS,row-NEIGHBORS):
        for j in range (NEIGHBORS,column-NEIGHBORS):
            firsti = i - NEIGHBORS
            firstj = j - NEIGHBORS  
            endi = i + NEIGHBORS + 1
            endj = j + NEIGHBORS + 1
            #print(str(firsti)+str(firstj)+str(endi)+str(endj)+"neighbors"+str(NEIGHBORS))
            newImage [m,n] = np.sum(image[firsti:endi,firstj:endj] * kernel[:,:])
            #print ("for2")
            n=n+1
        n=0
        m=m+1
    return newImage

def median(original,neighbor, borderline):
    rowO, columnO=original.shape
    #adiciona fila o columna a cada extremo y copia su valor correspondiente.
    #image = copy.deepcopy(original)
    image = original
    if ( borderline == 'reflejados'):
        image = np.pad(original,neighbor,'symmetric')
    elif ( borderline == 'ceros') :
        image = np.pad(original,neighbor, 'constant', constant_values=(0))
    row, column = image.shape
    #nueva imagen
    newImage = np.zeros((rowO,columnO))
    m = 0
    n = 0
    for i in range (neighbor,row-neighbor):
        for j in range (neighbor,column-neighbor):
            firsti = i - neighbor
            firstj = j - neighbor  
            endi = i + neighbor + 1
            endj = j + neighbor + 1
            #median
            vect = image[firsti:endi,firstj:endj].flatten()
            vect.sort()
            size = len(vect)
            median = vect[math.ceil(size / 2)]
            newImage[m,n] = median
            n=n+1
        n=0
        m=m+1
    return newImage  
