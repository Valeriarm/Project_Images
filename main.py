import tkinter as tk
from tkinter import messagebox
import pydicom
import numpy as np
import os
from matplotlib import pyplot as plt
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import libFilters
import windowFilters

VALUES = 65536
#debemos arreglar esta variable local
lstFilesDCM = []

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
    try:
        RefDs = pydicom.dcmread(lstFilesDCM[num])
    except:
        tk.messagebox.showinfo("Error", "No se encontraron archivos tipo DICOM.")
        return
    output ="En construccion...\n"
    try:
        output = "Imagen numero: " + str(num+1) + "\n"
        output = output + "Nombre: " + str(RefDs.PatientName) + "\n"
        output = output + "path: " + str(lstFilesDCM[num]) + "\n"
    except:
        output = output + "No hay nombre de paciente" + "\n"
    try:
        output = output + "PatientID: " + str(RefDs.PatientID) + "\n"
    except:
        output = output + "No hay id del paciente\n"
    try:
        output = output + "Columns: " + str(RefDs.Columns) + "\n"
    except:
        output = output + "No hay info de columnas\n"
    try:
        output = output + "Rows: " + str(RefDs.Rows) + "\n"
    except:
        output = output + "No hay info de filas\n"
    try:
        output = output + "Samples per pixel: " + str(RefDs.SamplesPerPixel) + "\n"
    except:
        output = output + "No hay info de muestras por pixel.\n"
    try:
        output = output + "Series Number: " + str(RefDs.SeriesNumber) + "\n"
    except:
        output = output + "No hay info del numero de serie.\n"
    try:
        output = output + "bitsAllocated: " + str(RefDs.BitsAllocated) + "\n"
    except:
        output = output + "No hay info de bitsAllocated.\n"
    try:
        output = output + "Manufacturer: " + str(RefDs.Manufacturer) + "\n"
    except:
        output = output + "No hay manufacturer.\n"
    try:
        output = output + "Largest: " + str(RefDs.LargestImagePixelValue) + "\n"
    except:
        output = output + "No hay info mayor valor de pixel.\n"
    try:
        output = output + "Smallest: " + str(RefDs.SmallestImagePixelValue) + "\n"
    except:
        output = output + "No hay info menor valor de pixel.\n"
    images.delete('1.0', 'end')
    images.insert('end', output)
    showImage(RefDs)

#poner un try por si no se cargan
def prepareDicoms(pathDicom):
    lstFilesDCM.clear()
    nextNum.config(text="0")
    #limpiar el canvas falta
    for dirName, subdirList, fileList in os.walk(pathDicom):
        for filename in fileList:
            if True or ".dcm" in filename.lower(): #check dicom
                lstFilesDCM.append(os.path.join(dirName,filename))
    images.delete('1.0', 'end')
    images.insert('end', str(len(lstFilesDCM)) + " imagenes.")


def folderFinder():
    folder = filedialog.askdirectory()
    if len(folder) <= 0:
            tk.messagebox.showinfo("Error", "Seleccione un directorio.")
            return
    else:
        lstFilesDCM = []
        prepareDicoms(folder)

def setHistogram():
    num = int(nextNum.cget("text"))
    try:
        refDs = pydicom.dcmread(lstFilesDCM[num])
    except:
        tk.messagebox.showinfo("Error", "No se encontraron archivos tipo DICOM.")
        return
    histogram = libFilters.histogram(refDs.pixel_array)
    plt.plot(histogram)
    plt.show()

def openFilterWindow():
    num = int(nextNum.cget("text"))
    if num == 0:
        messagebox.showerror("error", "No hay imagen seleccionada.")
        return
    refDs = pydicom.dcmread(lstFilesDCM[num])
    windowFilters.start(refDs.pixel_array,num,root)

def readNaturalImage():
    try:
        filepath = filedialog.askopenfilename()
    except:
        print ("esto no me habia pasado...")
        tk.messagebox.showinfo("Error", "Escoge una imagen.")
        return
    if not isinstance(filepath,str):
        tk.messagebox.showinfo("Error", "Escoge una imagen.")
        return
    image = Image.open(filepath).convert('L')
    windowFilters.start(np.array(image),0,root)

##GUI
root = tk.Tk()

#frames
frameL = tk.Frame(root, width = 50, height = 50)
frameR = tk.Frame(root, width = 50, height = 50)

#frameL
nextNum = tk.Label(frameL, text="0")
folderSelector = tk.Button(frameL, text="Seleccionar carpeta", command=folderFinder)
fileSelector = tk.Button(frameL, text="Seleccionar imagen", command=readNaturalImage)
filters = tk.Button(frameL,text="Aplicar Filtro", command=openFilterWindow)
inext = tk.Button(frameL, text="Siguiente",command= nextImage)
ibefore = tk.Button(frameL, text="Anterior", command= beforeImage)
histogram = tk.Button(frameL, text="Histograma", command= setHistogram)
images = tk.Text(frameL, height=20, width=50)
images.insert('end', "No hay imagenes seleccionadas")

#frameR
etiqueta = tk.Label(frameR, text="imagen dicom")

#pack frameL
frameL.pack(side = 'left')
#arreglar la posicion
folderSelector.pack(padx=2,pady= 2)
fileSelector.pack(padx=2,pady=2)
filters.pack(padx=5,pady=5)
images.pack(padx=5,pady=5)
histogram.pack(padx=5, pady=5,side='left')
nextNum.pack(padx=5,pady=5,side='right')
inext.pack(padx=2, side='right')
ibefore.pack(padx=5, pady=5, side='right')

#pack frameR
frameR.pack(side = 'right')
etiqueta.pack(side='top')



#\:v/
root.mainloop()