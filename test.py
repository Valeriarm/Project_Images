import tkinter as tk
import pydicom
import numpy as np
import os
from matplotlib import pyplot as plt
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#debemos arreglar esta variable local
lstFilesDCM = []
VALUES = 65536

def showImage(RefDs):
    #print(str(image.winfo_children()))#muestra que hay en el frame image
    #elimina lo que esta en ese frame
    for widget in frameR.winfo_children():
        widget.destroy()
    #crea el elemento que va a contener la imagen
    f = plt.Figure()
    a = f.add_subplot(111)
    a.imshow(RefDs.pixel_array, cmap=plt.cm.gray)
    imagesTemp = FigureCanvasTkAgg(f, master=frameR)
    imagesTemp.draw()
    imagesTemp.get_tk_widget().pack()

def beforeImage():
    num = int(nextNum.cget("text"))
    if num > 0:
        num = num-1
        accessImages(num)
        nextNum.config(text=num)
        


#next image
def nextImage():
    num = int(nextNum.cget("text"))
    if num < len(lstFilesDCM):
        num = num+1
        accessImages(num)
        nextNum.config(text=num)
        
    

#problema con la variable LstFileDCM
def accessImages(num):
    RefDs = pydicom.dcmread(lstFilesDCM[num])
    output ="En construccion...\n"
    #deberia poder hacer esto mejor porque puedo sacar los nombres de todos los atributos del header que tengo #20
    try:
        #output = output + "Tipos de Datos: " + str(RefDs.dir("")) + "\n" #muestra todos los datos que hay en el header por nombre
        output = output + "Imagen numero: " + str(num+1) + "\n"
        output = output + "Nombre: " + str(RefDs.PatientName) + "\n"
        output = output + "PatientID: " + str(RefDs.PatientID) + "\n"
        output = output + "Columns: " + str(RefDs.Columns) + "\n"
        output = output + "Rows: " + str(RefDs.Rows) + "\n"
        output = output + "Samples per pixel: " + str(RefDs.SamplesPerPixel) + "\n"
        output = output + "Series Number: " + str(RefDs.SeriesNumber) + "\n"
        output = output + "bitsAllocated: " + str(RefDs.BitsAllocated) + "\n"
        output = output + "Manufacturer: " + str(RefDs.Manufacturer) + "\n"
        output = output + "Largest: " + str(RefDs.LargestImagePixelValue) + "\n"
        output = output + "Smallest: " + str(RefDs.SmallestImagePixelValue) + "\n"
    except:
        #para saber cual es comenta uno a uno de los outputs
        output = "Algun dato no esta definido en el header."

    images.delete('1.0', 'end')
    images.insert('end', output)
    showImage(RefDs)

#poner un try por si no se cargan
def prepareDicoms(pathDicom):
    for dirName, subdirList, fileList in os.walk(pathDicom):
        for filename in fileList:
            if True or ".dcm" in filename.lower(): #check dicom
                lstFilesDCM.append(os.path.join(dirName,filename))
    images.delete('1.0', 'end')
    images.insert('end', str(len(lstFilesDCM)) + " imagenes.")

def folderFinder():
    folder = filedialog.askdirectory()
    prepareDicoms(folder)

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

##GUI
root = tk.Tk()

#frames
frameL = tk.Frame(root, width=350, height=500)
frameR = tk.Frame(root, width=350, height=500)

#frameR
nextNum = tk.Label(frameL, text="0")
folderSelector = tk.Button(frameL, text="Seleccionar carpeta", command=folderFinder)
inext = tk.Button(frameL, text="Siguiente",command= nextImage)
ibefore = tk.Button(frameL, text="Anterior", command=beforeImage)
histogram = tk.Button(frameL, text="Histograma", command= histogram)
fileSelector = tk.Button(frameL, text="Seleccionar imagen")
images = tk.Text(frameL, height=20, width=50)
images.insert('end', "No hay imagenes seleccionadas")

#frameR
etiqueta = tk.Label(frameR, text="imagen dicom")

#pack frameL
frameL.pack(side = 'left')
#arreglar la posicion
folderSelector.pack(padx=2,pady= 2)
fileSelector.pack(padx=2,pady=2)
images.pack(padx=5,pady=5)
histogram.pack(padx=5, pady=5,side='left')
nextNum.pack(padx=5,pady=5,side='right')
inext.pack(padx=2, side='right')
ibefore.pack(padx=5, pady=5, side='right')

#pack frameR
frameR.pack(side = 'right')
etiqueta.pack(side='top')
#canvas.pack()

#\:v/
root.mainloop()