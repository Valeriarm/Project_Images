#Procesamiento de Imagenes
#Integrantes: Valeria Rivera
#			  Emily Carvajal
#Lab 1

import tkinter as tk
import pydicom 
import numpy as np
import os
from matplotlib import pyplot as plt
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#debemos arreglar esta variable local
lstFilesDCM = []

def showImage(RefDs):
	#print(str(image.winfo_children()))#muestra que hay en el frame image
	#elimina lo que esta en ese frame
	for widget in image.winfo_children():
		widget.destroy()
	#crea el elemento que va a contener la imagen
	f = plt.Figure()
	a = f.add_subplot(111)
	a.imshow(np.flipud(RefDs.pixel_array),cmap=plt.cm.gray)
	imagesTemp = FigureCanvasTkAgg(f, master=image)
	imagesTemp.draw()
	imagesTemp.get_tk_widget().pack()


#problema con la variable LstFileDCM
def accessImages():
	num = int(inext.cget("text"))
	if num < len(lstFilesDCM):
		inext.config(text=num+1)

	RefDs = pydicom.dcmread(lstFilesDCM[num])
	output ="En construccion...\n"
	#deberia poder hacer esto mejor porque puedo sacar los nombres de todos los atributos del header que tengo #20
	try:	
		#output = output + "Tipos de Datos: " + str(RefDs.dir("")) + "\n" #muestra todos los datos que hay en el header por nombre
		output = output + "Imagen numero: " + str(num) + "\n"
		output = output + "PatientID: " + str(RefDs.PatientID) + "\n"
		output = output + "Columns: " + str(RefDs.Columns) + "\n"
		output = output + "Rows: " + str(RefDs.Rows) + "\n"
		output = output + "Series Number: " + str(RefDs.SeriesNumber) + "\n"
		output = output + "bitsAllocated: " + str(RefDs.BitsAllocated) + "\n"
		output = output + "Manufacturer: " + str(RefDs.Manufacturer) + "\n"
		output = output + "Manufacturer: " + str(RefDs.LargestImagePixelValue) + "\n"

		#output = output + "pixel lower range of pixels:  "+str(RefDs.SmallestImagePixelValue) + "\n"
	except:
		#para saber cual es comenta uno a uno de los outputs
		output = "Algun dato no esta definido en el header."

	images.delete('1.0', 'end')
	images.insert('end', output)
	showImage(RefDs)

#poner un try por si no se cargan
def prepareDicoms(pathDicom):
	#lstFilesDCM = [] #empty list
	for dirName, subdirList, fileList in os.walk(pathDicom):
	    for filename in fileList:
	        if ".dcm" in filename.lower(): #check dicom 
	            lstFilesDCM.append(os.path.join(dirName,filename))
	images.delete('1.0', 'end')
	images.insert('end', str(len(lstFilesDCM)) + " imagenes.")
	#print(str(lstFilesDCM))
	accessImages()


def folderFinder():
	folder = filedialog.askdirectory()
	prepareDicoms(folder)

##GUI
root = tk.Tk()

#frames
frame= tk.Frame(root, width=350, height=500)
image = tk.Frame(root, width=350, height=500)

#frame
titulo = tk.Label(frame, text="DICOM")
inext = tk.Label(frame, text="0")
boton = tk.Button(frame, text="Seleccionar imagenes", command=folderFinder)
next = tk.Button(frame, text="Siguiente",command= accessImages)
images = tk.Text(frame, height=20, width=50)
images.insert('end', "No hay imagenes seleccionadas")

#image
etiqueta = tk.Label(image, text="imagen dicom")

#pack frame
frame.pack(side = 'left')
titulo.pack(padx= 5 , pady = 5)
images.pack(padx=5,pady=5)
boton.pack(padx= 5,pady= 5,side='left')
inext.pack(padx=2, side='right')
next.pack(padx=5, pady=5, side='right')

#pack image
image.pack(side = 'right')
etiqueta.pack(side='top')
#canvas.pack()

#\:v/
root.mainloop()