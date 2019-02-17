#Procesamiento de Imagenes
#Integrantes: Valeria Rivera
#Lab 1

import tkinter as tk
from tkinter import ttk
import pydicom 
import numpy as np
import os
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
import math

lstFilesDCM = []
VALUES = 65536



def showImage(RefDs):
	for widget in frameR.winfo_children():
		widget.destroy()
	f = plt.Figure()
	a = f.add_subplot(111)
	a.imshow(RefDs.pixel_array, cmap=plt.cm.gray)
	imagesTemp = FigureCanvasTkAgg(f, master=frameR)
	imagesTemp.draw()
	imagesTemp.get_tk_widget().pack()


def accessImages(num):
	RefDs = pydicom.dcmread(lstFilesDCM[num-1])
	output ="En construccion...\n"

	try:	
		output = output + "Imagen numero: " + str(num) + "\n"
		output = output + "Nombre: " + str(RefDs.PatientName) + "\n"
		output = output + "PatientID: " + str(RefDs.PatientID) + "\n"
		output = output + "Columns: " + str(RefDs.Columns) + "\n"
		output = output + "Rows: " + str(RefDs.Rows) + "\n"
		output = output + "Samples per pixel: " + str(RefDs.SamplesPerPixel) + "\n"
		output = output + "Series Number: " + str(RefDs.SeriesNumber) + "\n"
		output = output + "bitsAllocated: " + str(RefDs.BitsAllocated) + "\n"
		output = output + "Manufacturer: " + str(RefDs.Manufacturer) + "\n"		
	except:
		output = "Algun dato no esta definido en el header."

	images.delete('1.0', 'end')
	images.insert('end', output)
	showImage(RefDs)



def nextI():
	num = int(inext.cget("text"))
	if num < len(lstFilesDCM):
		inext.config(text=num+1)

	accessImages(num)



def beforeI():
	num = int(inext.cget("text"))
	if (num <= len(lstFilesDCM) and num > 0):
		inext.config(text=num-1)

	accessImages(num)



def prepareDicoms(pathDicom):
	for dirName, subdirList, fileList in os.walk(pathDicom):
	    for filename in fileList:
	        if True or ".dcm" in filename.lower(): #check dicom 
	            lstFilesDCM.append(os.path.join(dirName,filename))
	images.delete('1.0', 'end')
	images.insert('end', str(len(lstFilesDCM)) + " imagenes.")
	nextI()


def folderFinder():
	folder = filedialog.askdirectory()
	prepareDicoms(folder)




#//////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////HISTOGRAM/////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////


def histogram():
	num = int(inext.cget("text"))
	RefDs = pydicom.dcmread(lstFilesDCM[num])
	image = RefDs.pixel_array
	hist = [0]*VALUES
	for i in range (0,RefDs.Columns-1):
		for j in range(0,RefDs.Rows-1):
			index = image[i][j]
			hist[index]+=1
	plt.plot(hist)
	plt.show()

#////////////////////////////////////////CONVOLUTION///////////////////////////////////////////


plt.figure(dpi=300)
plt.axes().set_aspect('equal')



def conv(image, kernel):
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

	return image_conv


def convolution():
	k=[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
	num = int(inext.cget("text"))
	RefDs = pydicom.dcmread(lstFilesDCM[num])
	image = RefDs.pixel_array
	conv(image,k)
	plt.imshow(conv(image,k), cmap=plt.cm.bone)
	plt.show()


#img=[[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]]
#k=[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]


#//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////SOBEL///////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////


def sobelFilter(image):

	sobelKernelX=[[-1,0,1],[-2,0,2],[-1,0,1]]
	sobelKernelY=[[-1,-2,-1],[0,0,0],[1,2,1]]

	gradientX= conv(image, sobelKernelX)
	gradientY= conv(image, sobelKernelX)

	gradient=[0]*len(image)
	angles=[0]*len(image)

	for i in range (len(image)):
		gradient[i] = [0]*len(image[0])
		angles[i] = [0]*len(image[0])

	for i in range (len(image)):
		for j in range(len(image[0])):
			gradient[i][j]=abs(gradientX[i][j])+abs(gradientY[i][j])
			#angles[i][j]=math.atan(gradientY[i][j]/gradientX[i][j])		

	return gradient#,angles


def sobel():
	num = int(inext.cget("text"))
	RefDs = pydicom.dcmread(lstFilesDCM[num])
	image = RefDs.pixel_array
	sobelFilter(image)
	plt.imshow(sobelFilter(image), cmap=plt.cm.bone)
	plt.show()



#//////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////THRESHOLDING/////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////


def thresholding(histograma):
	total = len(histograma)
	suma = float(0)
	sumaB = float(0)
	wB = 0
	wF = 0
	varMax=0
	threshold=0

	for i in range (VALUES):
		suma += i * histograma[i]

	for i in range (VALUES):
		wB += histograma[i]
		wF = total - wB

		if wF==0 :
			break

		sumaB += i*histograma[i]
		mB = sumaB / wB
		mF = (suma - sumaB) / wF
		varBetween = wB * wF * (mB - mF) * (mB - mF)

		if (varBetween > varMax):
			varMax = varBetween
			threshold = i

	return threshold



#//////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////GUI///////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////

root = Tk()

#frames
frameL = tk.Frame(root)
frameR = tk.Frame(root)
frameR2 = tk.Frame(root)


#///////////////////////LEFT FRAME////////////////////////
inext = tk.Label(frameL, text="0")
folderSelector = tk.Button(frameL,height=1 ,width=15 ,text="Seleccionar carpeta", command=folderFinder)
next = tk.Button(frameL,height=1 ,width=9 , text="Siguiente",command= nextI)
before = tk.Button(frameL,height=1 ,width=9 , text="Anterior", command= beforeI)
histogram = tk.Button(frameL,height=1 ,width=15 , text="Histograma", command= histogram)
fileSelector = tk.Button(frameL,height=1 ,width=15 , text="Seleccionar imagen", )
convolution = tk.Button(frameL,height=1 ,width=15 , text="Convolucion", command= convolution)
sobel = tk.Button(frameL,height=1 ,width=15 , text="Sobel", command= sobel)
images = tk.Text(frameL, height=20, width=30)
images.insert('end', "No hay imagenes seleccionadas")
filtros = ttk.Combobox(frameL,height=1 ,width=15)
kernelSize = ttk.Combobox(frameL,height=1 ,width=15)



#///////////////////////RIGTH FRAME////////////////////////
etiqueta = tk.Label(frameR, text="imagen dicom")
etiquetaFiltro = tk.Label(frameR2, text="imagen con filtro")


#///////////////////////PACKS////////////////////////
frameL.pack(side = 'left')
folderSelector.pack(padx=2,pady= 2, side = 'top')
fileSelector.pack(padx=2,pady=2, side = 'top')                                                                                                     
histogram.pack(padx=2, pady=2,side='top')
convolution.pack(padx=2, pady=2,side='top')
sobel.pack(padx=2, pady=2,side='top')
filtros.pack(padx=2, pady=2,side='top')
kernelSize.pack(padx=2, pady=2,side='top')

before.pack(padx=5, pady=10, side='left')
next.pack(padx=5, pady=10, side='left')
inext.pack(padx=2, side='left')


frameR.pack(side = 'right')
images.pack(padx=5,pady=5)
etiqueta.pack(side='top')
#canvas.pack()

#\:v/
root.mainloop()


