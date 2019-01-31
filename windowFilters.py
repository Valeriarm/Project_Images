import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import libFilters

#filterName["values"] = []
#KernelSize["values"] = []
sigma = []
kernels = [] #heave

def uploadKernels(filterName, kernelSize):
    div = 10
    archivo = open("kernel.txt","r")
    matrix = ''
    for line in archivo.readlines():
        fvalues = list(filterName["values"])
        kvalues = list(kernelSize["values"])
        if(line == "*\n"):
            if(matrix != ''):
                matrix = matrix[:-2]
                print("kernel")
                kernels.append(np.mat(matrix) * (1/div))
            matrix = ''
        elif(line.find("S") != -1):
            words = line.split(" ")
            #la primera es nombre, vecindad y sigma
            filterName["values"]=fvalues + [words[0]]
            kernelSize["values"]=kvalues + [words[1]]
            sigma.append(words[2][1:])
            div = float(words[3][:-1])
        else:
            items = line.split("\t")
            items[len(items)-1] = items[len(items)-1][:-1]#elimina el salto de linea
            for i in range(0,len(items)):
                matrix = matrix + items[i] + ' '
            matrix=matrix[:-1]
            matrix = matrix + '; ' 
    matrix = matrix[:-2]
    print("kernel")
    kernels.append(np.mat(matrix) * (1/div))
    #convierte la matrix a una numpy array
    print(filterName["values"])
    print(kernelSize["values"])
    print(len(kernels))
    archivo.close()

def start(refDs,num,root):
    filters = tk.Toplevel(root)
    #frame
    frameT = tk.Frame(filters,width=300,height=500)
    frameTL = tk.Frame(frameT, width=150, height=500)
    frameTR = tk.Frame(frameT,width=150,height=500)
    frameB = tk.Frame(filters,width=300,height=500)
    frameBL = tk.Frame(frameB, width=150, height=500)
    frameBR = tk.Frame(frameB, width=150,height=500)
    #frameTL
    title = tk.Label(frameTL, text="Filtros")
    numImage = tk.Label(frameTL,text="Imagen numero: "+str(num))
    filterName = ttk.Combobox(frameTL, state="readonly")
    kernelSize = ttk.Combobox(frameTL, state="readonly")
    apply = tk.Button(frameTL, text="Aplicar", command =lambda: applyFilter(frameBR, refDs, kernels[filterName.current()]))
    uploadKernels(filterName, kernelSize)
    #frameTR
    info = tk.Text(frameTR, height=11, width=50)
    #pack frameT
    frameT.pack(side='top')
    #
    frameTL.pack(side='left')
    title.pack(side='top',padx=5,pady=5)
    numImage.pack(padx=5,pady=5)
    filterName.pack(padx=5,pady=5)
    kernelSize.pack(padx=5,pady=5)
    apply.pack(padx=5,pady=5)
    #
    frameTR.pack(side='right')
    info.pack(padx=5,pady=5)
    showInfo(refDs,num, info)
    #pack frameB
    frameB.pack(side='bottom')
    #
    frameBL.pack(side = 'left')
    frameBR.pack(side='right')
    showImage(refDs,frameBL)
    showImage(refDs,frameBR)

def showInfo(refDs,num, info):
    output ="En construccion...\n"
    try:
        output = "Imagen numero: " + str(num+1) + "\n"
        output = output + "Nombre: " + str(refDs.PatientName) + "\n"
    except:
        output = output + "No hay nombre de paciente" + "\n"
    try:
        output = output + "PatientID: " + str(refDs.PatientID) + "\n"
    except:
        output = output + "No hay id del paciente\n"
    try:
        output = output + "Columns: " + str(refDs.Columns) + "\n"
    except:
        output = output + "No hay info de columnas\n"
    try:
        output = output + "Rows: " + str(refDs.Rows) + "\n"
    except:
        output = output + "No hay info de filas\n"
    try:
        output = output + "Samples per pixel: " + str(refDs.SamplesPerPixel) + "\n"
    except:
        output = output + "No hay info de muestras por pixel.\n"
    try:
        output = output + "Series Number: " + str(refDs.SeriesNumber) + "\n"
    except:
        output = output + "No hay info del numero de serie.\n"
    try:
        output = output + "bitsAllocated: " + str(refDs.BitsAllocated) + "\n"
    except:
        output = output + "No hay info de bitsAllocated.\n"
    try:
        output = output + "Manufacturer: " + str(refDs.Manufacturer) + "\n"
    except:
        output = output + "No hay manufacturer.\n"
    try:
        output = output + "Largest: " + str(refDs.LargestImagePixelValue) + "\n"
    except:
        output = output + "No hay info mayor valor de pixel.\n"
    try:
        output = output + "Smallest: " + str(refDs.SmallestImagePixelValue) + "\n"
    except:
        output = output + "No hay info menor valor de pixel.\n"
    info.delete('1.0', 'end')
    info.insert('end', output)

def showImage(RefDs,frame):
    #print(str(image.winfo_children()))#muestra que hay en el frame image
    #elimina lo que esta en ese frame
    for widget in frame.winfo_children():
        widget.destroy()
    #crea el elemento que va a contener la imagen
    f = plt.Figure()
    f.legend("Titulo")
    a = f.add_subplot(111)
    a.imshow(RefDs.pixel_array, cmap=plt.cm.gray)
    imagesTemp = FigureCanvasTkAgg(f, master=frame)
    imagesTemp.draw()
    imagesTemp.get_tk_widget().pack()

def showImageFiltered(image,frame):
    #print(str(image.winfo_children()))#muestra que hay en el frame image
    #elimina lo que esta en ese frame
    for widget in frame.winfo_children():
        widget.destroy()
    #crea el elemento que va a contener la imagen
    f = plt.Figure()
    a = f.add_subplot(111)
    print(image.shape)
    a.imshow(image, cmap=plt.cm.gray)
    imagesTemp = FigureCanvasTkAgg(f, master=frame)
    imagesTemp.draw()
    imagesTemp.get_tk_widget().pack()

def applyFilter(frame,refDs,kernel):
    print(len(kernel))
    newImage = libFilters.applyConvolution(refDs.pixel_array,kernel)
    showImageFiltered(newImage,frame)
