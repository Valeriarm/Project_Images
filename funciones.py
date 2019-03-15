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

VALUES = 65536

gaussian3x3 = np.array([[1,2,1],
						 [2,4,2],
						 [1,2,1]])


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
	
	for i in range(0,np.amax(image)):
		nu += i * histograma[i]

	for i in range(0,np.amax(image)):
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

	

