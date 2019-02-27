import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pydicom 
import numpy as np
import os, sys
import cv2
import math
import funciones


lstFilesDCM = []
VALUES = 65536
modifiedImage = np.zeros(512*512)


#////////////////ACCESS TO IMAGE///////////////////

def showOriginalImage(RefDs):
	for widget in frameR1.winfo_children():
		widget.destroy()
	f = plt.Figure()
	a = f.add_subplot(111)
	a.imshow(RefDs.pixel_array, cmap=plt.cm.gray)
	imagesDicom = FigureCanvasTkAgg(f, master=frameR1)
	imagesDicom.draw()
	imagesDicom.get_tk_widget().pack(padx=2,pady= 2, side = tk.LEFT, fill=tk.BOTH, expand=1)


def showFiletredImage(RefDs):
	f = plt.Figure()
	a = f.add_subplot(111)
	a.imshow(RefDs, cmap=plt.cm.gray)
	imagesFilteredDicom = FigureCanvasTkAgg(f, master=frameR)
	imagesFilteredDicom.draw()
	imagesFilteredDicom.get_tk_widget().pack(padx=2,pady= 2, side = tk.LEFT)



def accessImages(num):
	RefDs = pydicom.dcmread(lstFilesDCM[num-1])
	output = " "

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
		output = "Datos no definidos."

	infoImageDicom['text'] = output

	showOriginalImage(RefDs)



def prepareDicoms(pathDicom):
	lstFilesDCM.clear()
	inext.config(text = " 0 ")
	for dirName, subdirList, fileList in os.walk(pathDicom):
	    for filename in fileList:
	        if True or ".dcm" in filename.lower(): 
	            lstFilesDCM.append(os.path.join(dirName,filename))
	nextI()
	

def nextI():
	try:
		num = int(inext.cget("text"))
		if num < len(lstFilesDCM):
			inext.config(text=num+1)
		accessImages(num)
	except IndexError:
		messagebox.showerror("Warning", "No ha seleccionado una carpeta de imagenes")



def beforeI():
	try:
		num = int(inext.cget("text"))
		if (num <= len(lstFilesDCM) and num > 0):
			inext.config(text=num-1)
		accessImages(num)
	except IndexError:
		messagebox.showerror("Warning", "No ha seleccionado una carpeta de imagenes")


def folderFinder():
	folder = filedialog.askdirectory()
	prepareDicoms(folder)


#def imageFinder():
#	imageName = tk.filedialog.askopenfilename()
#	imageDicom = pydicom.dcmread(imageName)
	

#////////////////FUNTIONS////////////////////

def validationKernelFilterAndSize():
	try:
		imageFilter = filterSelector.get()
		kernelSize = kernelSelector.get()
		num = int(inext.cget("text"))
		RefDs = pydicom.dcmread(lstFilesDCM[num])
		image = RefDs.pixel_array

		if (imageFilter == "Gaussiano" and kernelSize == "3x3"):
			showFiletredImage(funciones.convolution(image,gaussian3x3))
		elif (imageFilter == "Gaussiano" and kernelSize == "5x5"):
			showFiletredImage(funciones.convolution(image,gaussian5x5))
		elif (imageFilter == "Gaussiano" and kernelSize == "7x7"):
			showFiletredImage(funciones.convolution(image,gaussian7x7))
		elif (imageFilter == "Promedio" and kernelSize == "3x3"):
			showFiletredImage(funciones.convolution(image,average3x3))
		elif (imageFilter == "Promedio" and kernelSize == "5x5"):
			showFiletredImage(funciones.convolution(image,average5x5))
		elif (imageFilter == "Promedio" and kernelSize == "7x7"):
			showFiletredImage(funciones.convolution(image,average7x7))
		elif (imageFilter == "Rayleigh" and kernelSize == "3x3"):
			showFiletredImage(funciones.convolution(image,rayleigh3x3))
		elif (imageFilter == "Rayleigh" and kernelSize == "5x5"):
			showFiletredImage(funciones.convolution(image,rayleigh5x5))
		elif (imageFilter == "Mediana" and kernelSize == "3x3"):
			showFiletredImage(funciones.median(image,median3x3))
		elif (imageFilter == "Mediana" and kernelSize == "5x5"):
			showFiletredImage(funciones.median(image,median5x5))
		elif (imageFilter == "Mediana" and kernelSize == "7x7"):
			showFiletredImage(funciones.median(image,median7x7))
		elif (imageFilter == "Mediana" and kernelSize == "9x9"):
			showFiletredImage(funciones.median(image,median9x9))
		elif (imageFilter == "Mediana" and kernelSize == "11x11"):
			showFiletredImage(funciones.median(image,median11x11))
		elif (imageFilter == "Mediana" and kernelSize == "13x13"):
			showFiletredImage(funciones.median(image,median13x13))
		elif (imageFilter == "Mediana" and kernelSize == "15x15"):
			showFiletredImage(funciones.median(image,median15x15))
		else:
			messagebox.showinfo("Warning", "Lo sentimos.. :( \n No esta disponible la opcion aun")
	except IndexError:
		messagebox.showerror("Warning", "No ha seleccionado una carpeta de imagenes")



def validationKernelSize():
	kernelSize = kernelSelector.get()
	if (kernelSize == "3x3"):
		return 1
	elif (kernelSize == "5x5"):
		return 2
	elif (kernelSize == "7x7"):
		return 3
	elif (kernelSize == "9x9"):
		return 5
	elif (kernelSize == "11x11"):
		return 7
	elif (kernelSize == "13x13"):
		return 9
	elif (kernelSize == "15x15"):
		return 11
	

def histogram():
	try:
		num = int(inext.cget("text"))
		RefDs = pydicom.dcmread(lstFilesDCM[num])
		histogram = funciones.histogram(RefDs)
		plt.plot(histogram)
		plt.show()
	except IndexError:
		messagebox.showerror("Warning", "No ha seleccionado una carpeta de imagenes")

def sobel():
	try:
		num = int(inext.cget("text"))
		RefDs = pydicom.dcmread(lstFilesDCM[num])
		image = RefDs.pixel_array
		neighbors = validationKernelSize()
		newImage = funciones.sobel(image, neighbors)
		plt.imshow(newImage, cmap=plt.cm.bone)
		plt.show()
	except IndexError:
		messagebox.showerror("Warning", "No ha seleccionado una carpeta de imagenes")



def otsu():
	
	num = int(inext.cget("text"))
	RefDs = pydicom.dcmread(lstFilesDCM[num])
	image = RefDs.pixel_array
	neighbors = validationKernelSize()
	newImage = funciones.sobel(image, neighbors)
	threshold = funciones.thresholding(newImage)
	#newImage = funciones.convolution(threshold, gaussian7x7)
	plt.imshow(threshold, cmap=plt.cm.bone)
	plt.show()






#///////////////////MATRIX/////////////////////

average3x3 = np.array([[1,1,1],
						[1,1,1],
						[1,1,1]])

average5x5 = np.array([[1,1,1,1,1],
						[1,1,1,1,1],
						[1,1,1,1,1],
						[1,1,1,1,1],
						[1,1,1,1,1]])

average7x7 = np.array([[1,1,1,1,1,1,1],
						[1,1,1,1,1,1,1],
						[1,1,1,1,1,1,1],
						[1,1,1,1,1,1,1],
						[1,1,1,1,1,1,1],
						[1,1,1,1,1,1,1],
						[1,1,1,1,1,1,1]])

gaussian3x3 = np.array([[1,2,1],
						 [2,4,2],
						 [1,2,1]])

gaussian5x5 = np.array([[1,4,7,4,1],
						 [4,16,26,16,4],
						 [7,26,41,26,7],
						 [4,16,26,16,4],
						 [1,4,7,4,1]])

gaussian7x7 = np.array([[0,0,1,2,1,0,0],
						 [0,3,13,22,13,3,0],
						 [1,13,59,97,59,13,1],
						 [2,22,97,159,97,22,2],
						 [1,13,59,97,59,13,1],
						 [0,3,13,22,13,3,0],
						 [0,0,1,2,1,0,0]])

rayleigh3x3 = np.array([[0,0,0],
							[0,367879,164169],
							[0,164169,73262]])

rayleigh5x5 = np.array([[0,0,0,0,0],
						   [0,367879,164169, 20213,813],
						   [0,164169,73262,9020,363],
						   [0,20213,9020,110,44],
						   [0,813,363,44,1

						   ]])

median3x3 = 1
median5x5 = 2
median7x7 = 3
median9x9 = 5
median11x11 = 7
median13x13 = 9
median15x15 = 11


#////////////////INTERFACE///////////////////

root = tk.Tk()

root.title("Filter Convertor")
root.configure(bg= "thistle1")
root.geometry("1000x500")


#Frames
frameL = tk.Frame(root,bg= "thistle1")
frameR = tk.Frame(root,bg= "thistle1")
frameR1 = tk.Frame(root,bg= "thistle1")
frameR2 = tk.Frame(root,bg= "thistle1")
frameNB = tk.Frame(frameL,bg= "thistle1")


#Valores de los Combobox
kernelSelectorValues = ["3x3","5x5","7x7", "9x9", "11x11", "13x13", "15x15"]
filterSelectorValues = ["Gaussiano","Promedio","Rayleigh","Mediana"]

#combobox style
comboStyle = ttk.Style()
comboStyle.theme_create('comboStyle',  parent = 'alt', settings = {'TCombobox': {'configure':{'fontground': 'gray58'}}})
comboStyle.theme_use('comboStyle')

#buttons
histogramButton = tk.Button(frameL,height=1 ,width=16 ,text="Histograma", bg= "gray58", fg = "white", font = "Arial 10", command = histogram)
sobelButton = tk.Button(frameL,height=1 ,width=16 ,text="Sobel", bg= "gray58", fg = "white", font = "Arial 10", command = sobel)
otsuButton = tk.Button(frameL,height=1 ,width=16 ,text="Otsu", bg= "gray58", fg = "white", font = "Arial 10", command = otsu)
folderSelector = tk.Button(frameL,height=1 ,width=16 ,text="Seleccionar carpeta", bg= "gray58", fg = "white", font = "Arial 10", command = folderFinder)
#imageSelector = tk.Button(frameL,height=1 ,width=16 ,text="Seleccionar imagen", bg= "gray58", fg = "white", font = "Arial 10", command = imageFinder)
aplyFilter = tk.Button(frameL,height=1 ,width=16 ,text="Aplicar Filtro", bg= "gray58", fg = "white", font = "Arial 10", command= validationKernelFilterAndSize)
nextButton = tk.Button(frameNB,height=1 ,width=8 ,text=">", bg= "gray58", fg = "white", font = "Arial 10 bold", command = nextI)
beforeButton = tk.Button(frameNB,height=1 ,width=8 ,text="<", bg= "gray58", fg = "white", font = "Arial 10 bold", command = beforeI)

#labels
kernelLabel = tk.Label(frameL, text="Tamano kernel",bg= "thistle1" , fg = "gray40", font = "Arial 10 bold")
filterLabel = tk.Label(frameL, text="Filtro", bg= "thistle1", fg = "gray40", font = "Arial 10 bold")
title = tk.Label(frameL,height=3, width=24, text="Procesamiento\nde Imagenes", bg= "thistle1", fg = "gray40", font = "Arial 15 bold")
inext = tk.Label(frameL, text="0", bg= "thistle1", fg = "gray40", font = "Arial 12 bold")
infoImageDicom = tk.Label(frameR, bg= "thistle1" ,text="Imagen Original", height=20, width=30,  fg = "gray30")


#comobox
kernelSelector = ttk.Combobox(frameL,height=1 ,width=15, values = kernelSelectorValues, state = "readonly", font = "Arial 11")
kernelSelector.current(0)
filterSelector = ttk.Combobox(frameL,height=1 ,width=15, values = filterSelectorValues, state = "readonly", font = "Arial 11")
filterSelector.current(0)



#////////////////////////////PACKS///////////////////////////

frameL.pack(side=tk.LEFT)
frameR.pack(side=tk.RIGHT)
frameR1.pack(side=tk.LEFT)
frameR2.pack(side=tk.RIGHT)


title.pack(padx=2,pady= 2,side=tk.TOP)
folderSelector.pack(padx=2,pady= 2,side=tk.TOP)
#imageSelector.pack(padx=2,pady= 2,side=tk.TOP)
histogramButton.pack(padx=2,pady= 2,side=tk.TOP)
sobelButton.pack(padx=2,pady= 2,side=tk.TOP)
otsuButton.pack(padx=2,pady= 2,side=tk.TOP)
kernelLabel.pack(padx=2,pady= 1,side=tk.TOP)
kernelSelector.pack(padx=2,pady= 1,side=tk.TOP)
filterLabel.pack(padx=2,pady= 1,side=tk.TOP)
filterSelector.pack(padx=2,pady= 1,side=tk.TOP)
aplyFilter.pack(padx=2,pady= 10,side=tk.TOP)
infoImageDicom.pack(padx=15,pady= 15,side=tk.RIGHT)

#botones de seguir
frameNB.pack(padx=2,pady= 10,side=tk.BOTTOM)
beforeButton.pack(padx=2,pady= 10,side=tk.LEFT)
nextButton.pack(padx=2,pady= 10,side=tk.LEFT)

inext.pack(padx=2,pady= 10,side=tk.BOTTOM)




root.mainloop()