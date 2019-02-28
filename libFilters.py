import numpy as np
import copy
import math
from matplotlib import pyplot as plt
from skimage import io
from numpy import linalg as LA

dicomImage = []

VALUES = 65536
NEIGHBORS = 1      

def histogram(matrix):
    row, column = matrix.shape
    max = np.amax(matrix)
    hist = np.zeros(max+1)#al ser resultado de una convolucion se sube el rango
    for i in range (0,row):
        for j in range(0,column):
            index = matrix[i][j]
            hist[index]+=1
    return hist

def applyConvolution(original,kernel,borderline):
    NEIGHBORS = int((len(kernel)/2)-0.5)
    #definir la cantidad de vecinos respecto al kernel escogido
    rowO, columnO=original.shape
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
            newImage [m,n] = np.sum(np.multiply(image[firsti:endi,firstj:endj], kernel[:,:]))
            n=n+1
        n=0
        m=m+1
    return newImage

def median(original,kernelSize, borderline):
    neighbor = math.floor(int(kernelSize)/2)
    rowO, columnO=original.shape
    #adiciona fila o columna a cada extremo y copia su valor correspondiente.
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


def otsu(filtered):
    total = filtered.size
    hist = histogram(filtered) #histogram
    #
    nu = 0
    sumB = 0
    wB = 0
    wF = 0
    threshold = 0
    varMax = 0
    for i in range(0,np.amax(filtered)): #imagen 1 brainDicom
        nu += i * hist[i]
    for i in range(0,np.amax(filtered)):#escoger uno
        wB += hist[i]
        if (wB == 0):
            continue
        wF = total - wB
        if (wF == 0): 
            break
        sumB += i * hist[i]
        mB = sumB / wB
        mF = (nu - sumB) / wF
        #calculate between class variance
        varBetween = wB * wF * (mB - mF) * (mB - mF)
        if (varMax < varBetween):
            varMax = varBetween
            threshold = i
    print ("threshold, ", threshold)
    #threshold divide entre blanco y negro
    row, column = filtered.shape
    for i in range(0,row):
        for j in range(0,column):
            if (filtered[i,j] >= threshold):
                filtered[i,j] = 65535
            elif( filtered[i,j] < threshold):
                filtered[i,j] = 0
    return filtered

def otsuParcial(original,kernelSize):
    print ("kernelSize,",kernelSize)
    neighbor = math.floor(int(kernelSize)/2)
    rowO, columnO=original.shape
    """ 
    image = original
    if ( borderline == 'reflejados'):
        image = np.pad(original,neighbor,'symmetric')
    elif ( borderline == 'ceros') :
        image = np.pad(original,neighbor, 'constant', constant_values=(0))
    row, column = image.shape """
    #nueva imagen
    newImage = np.zeros((rowO,columnO))
    m = 0
    n = 0
    for i in range (neighbor,rowO-neighbor):
        for j in range (neighbor,columnO-neighbor):
            firsti = i - neighbor
            firstj = j - neighbor  
            endi = i + neighbor + 1
            endj = j + neighbor + 1
            #otsu y threshold
            temp = otsu(original[firsti:endi,firstj:endj])
            newImage[firsti:endi,firstj:endj] = temp[:,:]
            n=n+1
        n=0
        m=m+1
    return newImage  
