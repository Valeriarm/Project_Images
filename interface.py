import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
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
modifiedImage = np.zeros((512,512))


#////////////////ACCESS TO IMAGE///////////////////

def showOriginalImage(RefDs):
	for widget in frameR1.winfo_children():
		widget.destroy()
	f = plt.Figure()
	a = f.add_subplot(111)
	a.imshow(RefDs.pixel_array, cmap=plt.cm.gray)
	imagesDicom = FigureCanvasTkAgg(f, master=frameR1)
	imagesDicom.draw()
	imagesDicom.get_tk_widget().pack(padx=2,pady= 2, side = tk.RIGHT)

def showFiletredImage(RefDs):
	global modifiedImage
	modifiedImage = RefDs
	f = plt.Figure()
	a = f.add_subplot(111)
	a.imshow(modifiedImage, cmap=plt.cm.gray)
	print(modifiedImage)
	imagesFilteredDicom = FigureCanvasTkAgg(f, master=frameR2)
	imagesFilteredDicom.draw()
	imagesFilteredDicom.get_tk_widget().pack(padx=2,pady= 2, side = tk.RIGHT)

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

	#infoImageDicom['text'] = output

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
		for widget in frameR2.winfo_children():
			widget.destroy()

		num = int(inext.cget("text"))
		if num < len(lstFilesDCM):
			inext.config(text=num+1)
		accessImages(num)
	except IndexError:
		messagebox.showerror("Warning", "No ha seleccionado una carpeta de imagenes")

def beforeI():
	try:
		for widget in frameR2.winfo_children():
			widget.destroy()

		num = int(inext.cget("text"))
		if (num <= len(lstFilesDCM) and num > 0):
			inext.config(text=num-1)
		accessImages(num)
	except IndexError:
		messagebox.showerror("Warning", "No ha seleccionado una carpeta de imagenes")

def folderFinder():
	folder = filedialog.askdirectory()
	prepareDicoms(folder)

	
#////////////////FUNTIONS////////////////////

def validationKernelFilterAndSize():
	global modifiedImage

	#try:
	for widget in frameR2.winfo_children():
		widget.destroy()
	imageFilter = filterSelector.get()
	kernelSize = kernelSelector.get()
	imageType = imageSelector.get()
	shape = shapeSelector.get()

	if (imageType == "Filtrada" and np.amax(modifiedImage) != 0):
		image = modifiedImage
	else:
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
	elif (imageFilter == "Sobel"):
		neighbors = validationKernelSize()
		showFiletredImage(funciones.sobel(image, neighbors))
	elif (imageFilter == "Otsu"):
		showFiletredImage(funciones.thresholding(image))
	elif(imageFilter == "Erosion" and shape == "Equis"):
		showFiletredImage(funciones.erosion(image, equis))
	elif(imageFilter == "Erosion" and shape == "Cruz"):
		showFiletredImage(funciones.erosion(image, cruz))
	elif(imageFilter == "Erosion" and shape == "Completa"):
		showFiletredImage(funciones.erosion(image, full))
	elif(imageFilter == "Dilatacion" and shape == "Equis"):
		showFiletredImage(funciones.dilatation(image, equis))
	elif(imageFilter == "Dilatacion" and shape == "Cruz"):
		showFiletredImage(funciones.dilatation(image, cruz))
	elif(imageFilter == "Dilatacion" and shape == "Completa"):
		showFiletredImage(funciones.dilatation(image, full))
	elif (imageFilter == "K-Means Color"):
		centroids = centroidsKmeans()
		showFiletredImage(funciones.kmeansColors(image, centroids))
	elif (imageFilter == "K-Means Grises"):
		centroids = centroidsKmeans()
		showFiletredImage(funciones.kmeansGrays(image, centroids))
	elif (imageFilter=="E-D"):
		showFiletredImage(applyDifference(image))
	else:
		messagebox.showinfo("Warning", "Lo sentimos.. :( \n No esta disponible la opcion aun")
	
	#except IndexError:
	#	messagebox.showerror("Warning", "Algo ha salido mal")

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

def validationColorGroup():
	colorGroup = colorSelector.get()
	if (colorGroup == "Grupo 0"):
		return 0
	elif (colorGroup == "Grupo 1"):
		return 1
	elif (colorGroup == "Grupo 2"):
		return 2
	elif (colorGroup == "Grupo 3"):
		return 3
	elif (colorGroup == "Grupo 4"):
		return 4
	elif (colorGroup == "Grupo 5"):
		return 5
	elif (colorGroup == "Grupo 6"):
		return 6
	elif (colorGroup == "Grupo 7"):
		return 7


def kmeansSeparation():
	global modifiedImage
	
	indexColor = validationColorGroup()
	imageType = imageSelector.get()

	if (imageType == "Filtrada"):
		image = np.copy(modifiedImage)
	else:
		messagebox.showinfo("Warning", "Primero filtre la imagen")
		num = int(inext.cget("text"))
		RefDs = pydicom.dcmread(lstFilesDCM[num])
		image = RefDs.pixel_array

	kmeanscolors = funciones.showOneColor(image,indexColor)
	#showFiletredImage(kmeanscolors)
	plt.imshow(kmeanscolors)
	plt.show()


def applyDifference(image):
    erosion = np.copy(funciones.erosion(image, full))
    dilatation = np.copy(funciones.dilatation(image, full))
    filtered = np.copy( dilatation - erosion )

    return filtered


def centroidsKmeans():
    answer = tk.simpledialog.askstring("Entrada", "Numero de centroides",parent=root)
    centroids = [0]*int(answer)
    tones = [0]*int(answer)
    if int(answer) < 0 or answer is None:
        tk.messagebox.showinfo("Error", "Ingrese  la cantidad de centroides")
        return 
    for i in range(0,int(answer)):
        data = tk.simpledialog.askstring("Entrada", "Centroide numero "+str(i)+":", parent=root)
        centroids[i] = int(data)

    return centroids


def histogram():
	try:
		global modifiedImage
		image = np.zeros((512,512))
		imageType = imageSelector.get()

		if (imageType == "Filtrada" and np.amax(modifiedImage)!= 0):
			image = modifiedImage
		else:
			num = int(inext.cget("text"))
			RefDs = pydicom.dcmread(lstFilesDCM[num])
			image = RefDs.pixel_array

		histogram = funciones.histogramNormalised(image)
		plt.plot(histogram)
		plt.show()
	except IndexError:
		messagebox.showerror("Warning", "No ha seleccionado una carpeta de imagenes")


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


#///////////////SHAPES EROSION AN DILATATION//////////////

full = np.array([[1,1,1],
						[1,1,1],
						[1,1,1]])

equis = np.array([[1,0,1],
						[1,1,1],
						[1,0,1]])

cruz = np.array([[0,1,0],
						[1,1,1],
						[0,1,0]])



#////////////////INTERFACE///////////////////

root = tk.Tk()

root.title("Filter Convertor")
root.configure(bg= "thistle1")
root.geometry("1000x500")


#Frames
frameL = tk.Frame(root,bg= "thistle1", width = 100, height=250)
frameR = tk.Frame(root,bg= "thistle1", width = 250, height=250 )
frameR1 = tk.Frame(root,bg= "thistle1", width = 250, height=250 )
frameR2 = tk.Frame(root,bg= "thistle1")
frameNB = tk.Frame(frameL,bg= "thistle1")


#Valores de los Combobox
kernelSelectorValues = ["3x3","5x5","7x7", "9x9", "11x11", "13x13", "15x15"]
filterSelectorValues = ["Gaussiano","Promedio","Mediana", "Sobel", "Otsu", "K-Means Color", "K-Means Grises", "Erosion", "Dilatacion", "E-D"]
shapeSelectorValues = ["Cruz", "Equis", "Completa"]
imageSelectorValues = ["Original", "Filtrada"]
colorSelectorValues = ["Grupo 0", "Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5", "Grupo 6", "Grupo 7"]

#combobox style
comboStyle = ttk.Style()
comboStyle.theme_create('comboStyle',  parent = 'alt', settings = {'TCombobox': {'configure':{'fontground': 'gray58'}}})
comboStyle.theme_use('comboStyle')

#buttons
histogramButton = tk.Button(frameL,height=1 ,width=16 ,text="Histograma", bg= "gray58", fg = "white", font = "Arial 10", command = histogram)
#sobelButton = tk.Button(frameL,height=1 ,width=16 ,text="Sobel", bg= "gray58", fg = "white", font = "Arial 10", command = sobel)
colorButton = tk.Button(frameL,height=1 ,width=16 ,text="Buscar Color", bg= "gray58", fg = "white", font = "Arial 10", command = kmeansSeparation)
folderSelector = tk.Button(frameL,height=1 ,width=16 ,text="Seleccionar carpeta", bg= "gray58", fg = "white", font = "Arial 10", command = folderFinder)
aplyFilter = tk.Button(frameL,height=1 ,width=17 ,text="Aplicar Filtro", bg= "gray58", fg = "white", font = "Arial 10", command= validationKernelFilterAndSize)
nextButton = tk.Button(frameNB,height=1 ,width=8 ,text=">", bg= "gray58", fg = "white", font = "Arial 10 bold", command = nextI)
beforeButton = tk.Button(frameNB,height=1 ,width=8 ,text="<", bg= "gray58", fg = "white", font = "Arial 10 bold", command = beforeI)

#labels
kernelLabel = tk.Label(frameL, text="Tamano kernel",bg= "thistle1" , fg = "gray40", font = "Arial 10 bold")
filterLabel = tk.Label(frameL, text="Filtro", bg= "thistle1", fg = "gray40", font = "Arial 10 bold")
imageLabel = tk.Label(frameL, text="Imagen", bg= "thistle1", fg = "gray40", font = "Arial 10 bold")
shapeLabel = tk.Label(frameL, text="Forma", bg= "thistle1", fg = "gray40", font = "Arial 10 bold")
title = tk.Label(frameL,height=3, width=24, text="Procesamiento\nde Imagenes", bg= "thistle1", fg = "gray40", font = "Arial 15 bold")
inext = tk.Label(frameL, text="0", bg= "thistle1", fg = "gray40", font = "Arial 12 bold")
colorLabel = tk.Label(frameL, text="Color por Grupo", bg= "thistle1", fg = "gray40", font = "Arial 10 bold")
#nfoImageDicom = tk.Label(frameR, bg= "thistle1" ,text="Imagen Original", height=20, width=30,  fg = "gray30")



#comobox
kernelSelector = ttk.Combobox(frameL,height=2 ,width=16, values = kernelSelectorValues, state = "readonly", font = "Arial 11")
kernelSelector.current(0)
filterSelector = ttk.Combobox(frameL,height=2 ,width=16, values = filterSelectorValues, state = "readonly", font = "Arial 11")
filterSelector.current(0)
imageSelector = ttk.Combobox(frameL,height=2 ,width=16, values = imageSelectorValues, state = "readonly", font = "Arial 11")
imageSelector.current(0)
shapeSelector = ttk.Combobox(frameL,height=2 ,width=16, values = shapeSelectorValues, state = "readonly", font = "Arial 11")
shapeSelector.current(0)
colorSelector = ttk.Combobox(frameL,height=2 ,width=16, values = colorSelectorValues, state = "readonly", font = "Arial 11")
colorSelector.current(0)



#////////////////////////////PACKS///////////////////////////

frameL.pack(side=tk.LEFT)
#frameR.pack(side=tk.RIGHT)
frameR2.pack(side=tk.LEFT)
frameR1.pack(side=tk.LEFT)



title.pack(padx=2,pady= 3,side=tk.TOP)
folderSelector.pack(padx=2,pady= 3,side=tk.TOP)
#imageSelector.pack(padx=2,pady= 2,side=tk.TOP)
histogramButton.pack(padx=2,pady= 10,side=tk.TOP)
#sobelButton.pack(padx=2,pady= 2,side=tk.TOP)
colorLabel.pack(padx=2,pady= 3,side=tk.TOP)
colorSelector.pack(padx=2,pady= 3,side=tk.TOP)
colorButton.pack(padx=2,pady= 2,side=tk.TOP)
kernelLabel.pack(padx=2,pady= 3,side=tk.TOP)
kernelSelector.pack(padx=2,pady= 3,side=tk.TOP)
filterLabel.pack(padx=2,pady= 3,side=tk.TOP)
filterSelector.pack(padx=2,pady= 3,side=tk.TOP)
imageLabel.pack(padx=2,pady= 3,side=tk.TOP)
imageSelector.pack(padx=2,pady=3,side=tk.TOP)
shapeLabel.pack(padx=2,pady= 3,side=tk.TOP)
shapeSelector.pack(padx=2,pady=3,side=tk.TOP)
aplyFilter.pack(padx=2,pady= 12,side=tk.TOP)
#infoImageDicom.pack(padx=15,pady= 15,side=tk.RIGHT)

#botones de seguir
frameNB.pack(padx=2,pady= 10,side=tk.BOTTOM)
beforeButton.pack(padx=2,pady= 10,side=tk.LEFT)
nextButton.pack(padx=2,pady= 10,side=tk.LEFT)

inext.pack(padx=2,pady= 10,side=tk.BOTTOM)




root.mainloop()