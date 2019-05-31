import numpy as np
import copy
import math
from matplotlib import pyplot as plt
from skimage import io
from numpy import linalg as LA

dicomImage = []

VALUES = 65536
NEIGHBORS = 1  

color1 = [0,0,0] #negro
color2 = [0,50,0] #verde
color3 = [255,0,0]#rojo
color4 =  [0,0,100]#azul
color5 = [255,255,255] #blanco
color6 = [255,255,0]#amarillo
color7 = [255,0,255]#rosa
color8 = [0,255,0]#neon
color =  [color1, color2, color3, color4, color5,color6, color7,color8]


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
    NEIGHBORS = int(np.floor(len(kernel)/2))
    rowO, columnO=original.shape
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
            newImage [m,n] = np.sum(np.multiply(image[firsti:endi,firstj:endj], kernel[:,:]))
            n=n+1
        n=0
        m=m+1
    return newImage

def median(original,kernelSize, borderline):
    neighbor = math.floor(int(kernelSize)/2)
    rowO, columnO=original.shape
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
                filtered[i,j] = 1
            elif( filtered[i,j] < threshold):
                filtered[i,j] = 0
    return filtered

def otsuParcial(original,kernelSize):
    neighbor = math.floor(int(kernelSize)/2)
    rowO, columnO=original.shape
    newImage = np.zeros((rowO,columnO))
    for i in range (neighbor,rowO+neighbor, kernelSize):
        for j in range (neighbor,columnO+neighbor, kernelSize):
            print(i, "  ", j)
            firsti = i - neighbor
            firstj = j - neighbor  
            endi = i + neighbor + 1
            endj = j + neighbor + 1
            #otsu y threshold
            temp = otsu(original[firsti:endi,firstj:endj])
            newImage[firsti:endi,firstj:endj] = temp[:,:]
    return newImage  

def Kmeans(matrix, centroids):
    pregroups = [[] for i in range(len(centroids))]
    d = np.zeros(len(centroids),dtype=int)
    cmin = 65536
    row, column = matrix.shape
    prematrix = np.zeros((row,column))
    for i in range(0,row):
        for j in range(0,column):
            #minimo
            for k in range(0,len(centroids)):
                d[k] = abs(centroids[k] - matrix[i,j])
            indexMinimun = d.argmin()
            prematrix[i,j] = indexMinimun
            pregroups[indexMinimun].append(matrix[i,j])

    #calculando centroides nuevos
    newCentroids = np.zeros(len(centroids),dtype=int)
    for i in range(0,len(centroids)):
        try:
            newCentroids[i] = int(np.sum(pregroups[i]) / len(pregroups[i]))
        except:
            newCentroids[i] = int(np.sum(pregroups[i]))
    return np.array_equiv(centroids, newCentroids), pregroups, newCentroids, prematrix    

def showOneColor(matrix, selectedColorIndex):
    global color
    background = [0,0,0]
    #escoger fondo
    if (np.array_equiv(color[selectedColorIndex],[0,0,0])):
        background = [255,255,255]
    row, column, _ = matrix.shape
    oneColor = np.copy(matrix)
    for i in range(0,row):
        for j in range(0,column):
            if ( not np.array_equiv(matrix[i,j],color[selectedColorIndex])):
                oneColor[i,j] = background
    return oneColor 

def applyGroups(matrix, groups, indexmatrix, centroids):
    global color
    #pintar
    row, column = matrix.shape
    colorsMatrix = np.zeros(shape=(row,column,3))#rgb
    
    for i in range(0, row):
        for j in range(0,column):
            for k in range(0,len(centroids)):
                if (k == indexmatrix[i,j]):
                    colorsMatrix[i,j] = color[k]

    return colorsMatrix           

def erosion(matrix, struct):
    neighbor = math.floor(int(len(struct))/2)
    rowO, columnO=matrix.shape
    row, column = struct.shape
    newImage = np.zeros((rowO,columnO))
    change = np.zeros((row,column))
    for i in range (neighbor,rowO-neighbor):
        for j in range (neighbor,columnO-neighbor):
            firsti = i - neighbor
            firstj = j - neighbor  
            endi = i + neighbor + 1
            endj = j + neighbor + 1
            #erosion    
            if ( not np.array_equiv(matrix[firsti:endi,firstj:endj], struct[:,:])):
                #pero debo tener en cuenta si en la nueva ya ahi unos marcados en ese sector
                if (np.sum(newImage[firsti:endi,firstj:endj]) == 0):
                    newImage[firsti:endi,firstj:endj] = change[:,:]
            else:
                #no debo quitar marcas realizadas
                newImage[i,j] = 1
    return newImage

def dilatation(matrix, struct):
    neighbor = math.floor(int(len(struct))/2)
    rowO, columnO=matrix.shape
    row, column = struct.shape
    newImage = np.zeros((rowO,columnO))
    change = np.ones((row,column))
    for i in range (neighbor,rowO-neighbor):
        for j in range (neighbor,columnO-neighbor):
            firsti = i - neighbor
            firstj = j - neighbor  
            endi = i + neighbor + 1
            endj = j + neighbor + 1
            #dilatation   
            # se esta suponiendo origen centro debo tener en cuenta opcion de centro 
            if ( matrix[i,j] == 1 ):
                newImage[firsti:endi,firstj:endj] = change[:,:]
    return newImage