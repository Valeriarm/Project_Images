import tkinter as tk 
from tkinter import ttk
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pydicom 
import numpy as np
import os, sys
import cv2
import math
import copy
import math
from scipy.spatial import distance_matrix

VALUES = 65536

gaussian3x3 = np.array([[1,2,1],
						 [2,4,2],
						 [1,2,1]])


rgbList= [[255,255,255],[0,0,0],[0,255,0],[0,0,255],[0,255,255],[255,0,255],[255,0,0],[0,255,255]]


def histogramNormalised(matrix):
    row, column = matrix.shape
    imageSize = row*column
    max = np.amax(matrix)
    hist = np.zeros(256)
    print(max)
    for i in range (0,row):
        for j in range(0,column):
            index = (matrix[i][j]/max)*255
            hist[index.astype(int)]+=1
            
    for i in range (0,len(hist)):
    	hist[i]=hist[i]/imageSize

    return hist


def histogram(matrix):
    row, column = matrix.shape
    max = np.amax(matrix)
    hist = np.zeros(max+1)

    for i in range (0,row):
        for j in range(0,column):
            index = matrix[i][j]
            hist[index]+=1

    return hist


def histogramMatrix(image):
	hist = np.zeros(VALUES)
	maxValue=0
	for i in range (0,len(image)):
		for j in range(0,len(image[0])):
			index = image[i][j]
			hist[index]+=1
			if (maxValue < hist[index]):
				maxValue = hist[index]
	return hist


def convolution(image, kernel):
	neighbors = len(kernel)//2
	newImage = [0]*len(image)

	for i in range (len(image)):
		newImage[i] = [0]*len(image[0])

	newImage= np.array(newImage)

	for i in range (neighbors, len(image)-neighbors):
		for j in range (neighbors,len(image[0])-neighbors):
			newImage[i-neighbors, j-neighbors]=np.sum(np.multiply(image[i-neighbors:i+neighbors+1,j-neighbors:j+neighbors+1],kernel[:,:]))
	return newImage


def sobel(imagen, neighbors):
	sobelKernelX=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
	sobelKernelY=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
	gradientX= convolution(imagen, sobelKernelX)
	gradientY= convolution(imagen, sobelKernelX)
	gradient = np.absolute(gradientX) + np.absolute(gradientY)
	gradient = gradient.astype(np.int64)

	return gradient


def median(image, neighbors):
	newImage = [0]*len(image)

	for i in range (len(image)):
		newImage[i] = [0]*len(image[0])

	newImage= np.array(newImage)

	for i in range (neighbors, len(image)-neighbors):
		for j in range (neighbors,len(image[0])-neighbors):
			orderList = image[i-neighbors:i+neighbors+1,j-neighbors:j+neighbors+1].flatten()
			orderList.sort()
			size = len(orderList)
			median = orderList[math.ceil(size / 2)]
			newImage[i][j] = median

	return newImage


def thresholding(image):
	total = image.size
	suma = sumaB= nu = 0
	wB = wF = varMax = threshold = 0
	histograma = histogram(image)
	#print(np.amax(image))
	
	for i in range(50,np.amax(image)):
		nu += i * histograma[i]

	for i in range(50,np.amax(image)):
		wB += histograma[i]
		if (wB == 0):
			continue
		wF = total - wB
		if (wF == 0): 
			break

		sumaB += i * histograma[i]
		mB = sumaB / wB
		mF = (nu - sumaB) / wF

		varBetween = wB*wF*(mB-mF)*(mB-mF)
		if (varMax < varBetween):
			varMax = varBetween
			threshold = i

		print (threshold)

	row, column = image.shape
	for i in range(0,row):
		for j in range(0,column):
			if (image[i,j] >= threshold):
				image[i,j] = 1
			elif( image[i,j] < threshold):
				image[i,j] = 0

	return image


def erosion(image, struct):
    neighbor = math.floor(int(len(struct))/2)
    rowO, columnO=image.shape
    row, column = struct.shape
    newImage = np.zeros((rowO,columnO))
    change = np.zeros((row,column))

    for i in range (neighbor,rowO-neighbor):
        for j in range (neighbor,columnO-neighbor):
            if ( not np.array_equiv(image[i - neighbor:i + neighbor + 1,j - neighbor:j + neighbor + 1], struct[:,:])):
                if (np.sum(newImage[i - neighbor:i + neighbor + 1,j - neighbor:j + neighbor + 1]) == 0):
                    newImage[i - neighbor:i + neighbor + 1,j - neighbor:j + neighbor + 1] = change[:,:]
            else:
                newImage[i,j] = 1

    return newImage


def dilatation(image, struct):
    neighbor = math.floor(int(len(struct))/2)
    rowO, columnO = image.shape
    row, column = struct.shape
    newImage = np.zeros((rowO,columnO))
    change = np.ones((row,column))

    for i in range (neighbor,rowO-neighbor):
        for j in range (neighbor,columnO-neighbor):
            if ( image[i,j] == 1 ):
                newImage[i - neighbor:i + neighbor + 1,j - neighbor:j + neighbor + 1] = change[:,:]

    return newImage


def calcularGrupo(imageValue, centroids):
    diferences = [0 for i in range (0,len(centroids))]

    for i in range  (0, len(centroids)):
        diferences[i] = np.absolute(imageValue - centroids[i])


    index = diferences.index(min(diferences))

    return index


def calcularCentroidesNuevos(image, centroids):
    groupsImage = image.copy()
    rows, columns = image.shape
    groupsToNewCentroids = [[] for i in range (len(centroids))]

    for i in range (0, rows):
        for j in range (0, columns):
            groupsImage[i][j]=calcularGrupo(image[i][j], centroids)
            groupsToNewCentroids[groupsImage[i][j]].append(image[i][j])



    newCentroids = [0 for i in range (0,len(centroids))]

    for i in range(0, len(centroids)):
        try:
            newCentroids[i] = (int(sum(groupsToNewCentroids[i]) / len(groupsToNewCentroids[i])))
        except(ZeroDivisionError):
            newCentroids[i] = (int(sum(groupsToNewCentroids[i])))

    print(newCentroids) 
    state = newCentroids!=centroids

    return state,  newCentroids, groupsToNewCentroids, groupsImage


def kmeansColors(image, centroids):   
    state, newCentroids, groups, groupsMatrix = calcularCentroidesNuevos(image, centroids)
    print("entro")
    while state:
        state, newCentroids, groups, groupsMatrix = calcularCentroidesNuevos(image, newCentroids)        

    print("terminooo")

    rows, columns = groupsMatrix.shape
    colorImage = [0]*len(groupsMatrix)

    for i in range (len(groupsMatrix)):
        colorImage[i] = [0]*len(groupsMatrix[0])
        for j in range (len(groupsMatrix[0])):
            colorImage[i][j] = [0,0,0]

    for i in range(0, rows):
        for j in range (0, columns):
            for k in range (0, len(newCentroids)):
                if (groupsMatrix[i][j]==newCentroids.index(newCentroids[k])):
                    colorImage[i][j]= rgbList[k]


    return colorImage


def kmeansGrays(image, centroids):   
    state, newCentroids, groups, groupsMatrix = calcularCentroidesNuevos(image, centroids)
    print("entro")
    while state:
        state, newCentroids, groups, groupsMatrix = calcularCentroidesNuevos(image, newCentroids)        

    print("terminooo")

    rows, columns = groupsMatrix.shape

    for i in range(0, rows):
        for j in range (0, columns):
            for k in range (0, len(newCentroids)):
                if (groupsMatrix[i][j]==newCentroids.index(newCentroids[k])):
                    groupsMatrix[i][j]= neighbors[k]

    return groupsMatrix



def showOneColor(image, group):
    colorImage  = np.copy(image)
    background= [255,255,255]
    groupColor = rgbList[group]

    if (groupColor==background):
        background=[0,0,0]

    for i in range(0, len(image)):
        for j in range (0, len(image[0])):
            print(image[i][j])
            if ( not np.array_equiv(image[i][j], groupColor)):
                colorImage[i][j] = background

    return colorImage


