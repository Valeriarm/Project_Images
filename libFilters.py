import numpy as np
from matplotlib import pyplot as plt
from skimage import io

dicomImage = []

VALUES = 65536
NEIGHBORS = 1
KERNELGAUSS3 = np.array([[0, 0, 0],
                        [0, 0.367879, 0.164169],
                        [0, 0.164169, 0.073262]])

KERNELGAUSS7 = np.array([[0.000036,0.000363,0.001446,0.002291,0.001446,0.000363,0.000036],
                [0.000363,0.003676,0.014662,0.023226,0.014662,0.003676,0.000363],
                [0.001446,0.014662,0.058488,0.092651,0.058488,0.014662,0.001446],
                [0.002291,0.023226,0.092651,0.146768,0.092651,0.023226,0.002291],
                [0.001446,0.014662,0.058488,0.092651,0.058488,0.014662,0.001446],
                [0.000363,0.003676,0.014662,0.023226,0.014662,0.003676,0.000363],
                [0.000036,0.000363,0.001446,0.002291,0.001446,0.000363,0.000036]])

def histogram(refDs):
    image = refDs.pixel_array
    hist = [0]*VALUES
    for i in range (0,refDs.Columns-1):
        for j in range(0,refDs.Rows-1):
            index = image[i][j]
            hist[index]+=1
    return hist

def averageKernel(num):
    kerne = np.ones((num,num)) #filtro mediana - promedio
    l = 1.0/(num*num)
    kernel = kerne * l
    return kernel

def applyConvolution(original,kernel):
    #kernel = getKernel(kernelName)
    NEIGHBORS = int((len(kernel)/2)-0.5)
    #print(str(isinstance(NEIGHBORS,int)))
    #definir la cantidad de vecinos respecto al kernel escogido
    rowO, columnO=original.shape
    #print("row"+str(rowO)+"\ncolumn"+str(columnO)+str(NEIGHBORS))
    #adiciona fila o columna a cada extremo y copia su valor correspondiente.
    image = np.pad(original,NEIGHBORS,'symmetric')
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