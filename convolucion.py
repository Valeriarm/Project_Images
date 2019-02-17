import tkinter as tk
import pydicom 
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt


image = os.path.join("C:/Users/Asus/Documents/Procesamiento/MRI Images/","MRI22.dcm")
RefDs = pydicom.dcmread(image)

plt.figure(dpi=300)
plt.axes().set_aspect('equal')

#plt.imshow(RefDs.pixel_array, cmap=plt.cm.bone)

def conv_transform(image):
	image_copy = image.copy()

	for i in range (len(image)):
		for j in range(len(image[0])):
			image_copy[i][j] = image[len(image)-i-1][len(image[0])-j-1]
	return image_copy


def conv(image, kernel1):

	kernel=conv_transform(kernel1)

	image_h=len(image)
	image_w=len(image[0])

	kernel_h=len(kernel)
	kernel_w=len(kernel[0])

	h=kernel_h//2
	w=kernel_w//2

	image_conv=[0]*len(image)

	for i in range (len(image)):
		image_conv[i] = [0]*len(image[0])

	for i in range(h,image_h-h):
		for j in range(w, image_w-w):
			sum=0

			for m in range(kernel_h):
				for n in range(kernel_w):
					sum=sum+kernel[m][n]+image[i-h+m][j-w+n]

			image_conv[i][j]=sum

	print(image_conv)
	return image_conv



img=[[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]]
k=[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]

#conv(RefDs.pixel_array,k)
plt.imshow(conv(RefDs.pixel_array,k), cmap=plt.cm.bone)
plt.show()