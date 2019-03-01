import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import libFilters

sigma = []
kernels = [] #heave

SOBELX = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

SOBELY = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]]) 
filtered = np.ones((512,512))

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
                #print("kernel")
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
    kernels.append(np.mat(matrix) * (1/div))
    #convierte la matrix a una numpy array
    archivo.close()

def start(refDs,num,root):
    filters = tk.Toplevel(root)
    #frame
    frameT = tk.Frame(filters,width=250,height=400)
    frameTBorder = tk.Frame(frameT, width=100, height=100)
    frameTPrepro = tk.Frame(frameT, width=100, height=100, highlightcolor="black", highlightthickness=1)
    frameTFilter = tk.Frame(frameT,width=100,height=100)
    frameB = tk.Frame(filters,width=250,height=400)
    frameBL = tk.Frame(frameB, width=100, height=400)
    frameBR = tk.Frame(frameB, width=100,height=400)
    #frameBorder
    titleBorder = tk.Label(frameTBorder, text="Borderline")
    comboBorder = ttk.Combobox(frameTBorder, state="readonly")
    comboBorder["values"]=["ignorar","reflejados","ceros"]
    #frameTPrepro
    title = tk.Label(frameTPrepro, text="Preprocessing")
    numImage = tk.Label(frameTPrepro,text="Imagen numero: "+str(num))
    filterName = ttk.Combobox(frameTPrepro, state="readonly")
    kernelSize = ttk.Combobox(frameTPrepro, state="readonly")
    apply = tk.Button(frameTPrepro, text="Aplicar Prepro", command =lambda: applyFilter(frameBR, refDs, filterName.current(),kernelSize.get(),comboBorder.get()))
    uploadKernels(filterName, kernelSize)
    #frameTFilter
    titleTFilter = tk.Label(frameTFilter, text="Filtros")
    filterTFilter = ttk.Combobox(frameTFilter, state="readonly")
    applyF = tk.Button(frameTFilter, text="Aplicar Filtro", command = lambda: wichOne(filterTFilter.get(),kernelSize.get(),comboBorder.get(),frameBR))
    cut = tk.Button(frameTFilter, text="recortar", command = lambda: cutImage(frameBL))
    filterTFilter["values"] =["Sobel","Otsu", "OtsuParcial"]
    #pack ############################
    frameT.pack(side='top')
    #FrameBorder
    frameTBorder.pack(side='left', padx=5, pady=5)
    titleBorder.pack(side='top', padx=5,pady=5)
    comboBorder.pack(padx=5,pady=5)
    #frameTPrepro
    frameTPrepro.pack(side='left', padx=5, pady=5)
    title.pack(side='top',padx=5,pady=5)
    numImage.pack(padx=5,pady=5)
    filterName.pack(padx=5,pady=5)
    kernelSize.pack(padx=5,pady=5)
    apply.pack(padx=5,pady=5)
    #frameTFilter
    frameTFilter.pack(side='left', padx=5, pady=5)
    titleTFilter.pack(side = 'top', padx=5, pady=5)
    filterTFilter.pack(padx=5,pady=5)
    applyF.pack(padx=5,pady=5)
    cut.pack(padx=5,pady=5)
    #pack frameB
    frameB.pack(side='bottom')
    #frameB
    frameBL.pack(side = 'left')
    frameBR.pack(side='left')
    #
    showImage(refDs,frameBL)
    showImage(refDs,frameBR)

def showImage(RefDs,frame):
    #print(str(image.winfo_children()))#muestra que hay en el frame image
    #elimina lo que esta en ese frame
    for widget in frame.winfo_children():
        widget.destroy()
    #crea el elemento que va a contener la imagen
    f = plt.Figure()
    f.legend("Titulo")
    a = f.add_subplot(111)
    a.imshow(RefDs, cmap=plt.cm.gray)
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
    a.imshow(image, cmap=plt.cm.gray)
    imagesTemp = FigureCanvasTkAgg(f, master=frame)
    imagesTemp.draw()
    imagesTemp.get_tk_widget().pack()

def applyFilter(frame,refDs,kernelNum,kernelSize,borderline):
    global filtered
    if (kernelNum == 1 or kernelNum == 2 or kernelNum == 3 or kernelNum == 11):#mejorar esta escogencia.
        #recuperar el tamaño del kernel correspondiente a la matrix seleccionada
        newImage = libFilters.median(refDs,kernelSize,borderline)
        #ver si si cambio resta de original y filtrada de media
        '''
        r = refDs.pixel_array - newImage
        plt.imshow(r, cmap=plt.cm.gray)
        plt.show()
        '''
    else:
        kernel = kernels[kernelNum]
        newImage = libFilters.applyConvolution(refDs,kernel,borderline)
    newImage = newImage.astype(np.int64)#
    #filtered = copy.deepcopy(newImage) 
    filtered = newImage
    showImageFiltered(newImage,frame)

def wichOne (name,kernelSize,borderline, frame):
    #filterTFilter.get(),kernelSize.get(), comboBorder.get(),frameBR)
    if(name == 'Sobel'):
        sobel(borderline,frame)
    elif(name == 'Otsu'):
        applyOtsu(frame)
    elif(name=='OtsuParcial'):
        applyOtsuParcial(20,frame)
        

#deberia normalizar?
def sobel(borderline,frame):
    global filtered
    gx = libFilters.applyConvolution(filtered, SOBELX, borderline)
    gy = libFilters.applyConvolution(filtered, SOBELY, borderline)
    g = np.absolute(gx) + np.absolute(gy)
    g = g.astype(np.int64)#
    filtered = np.copy(g)

    showImageFiltered(g,frame)
    

def applyOtsu(frame):
    global filtered
    filtered = np.copy(libFilters.otsu(filtered))
    #filtered = np.copy(filtered)
    showImageFiltered(filtered,frame)

def applyOtsuParcial(kernelSize,frame):
    global filtered
    filtered = np.copy(libFilters.otsuParcial(filtered, kernelSize))
    print("termino otsu parcial")
    showImageFiltered(filtered,frame)

#funciona una vez otsu tiene errores :v
def cutImage(frame):
    global filtered
    min = 512
    row, column = filtered.shape
    x = 0
    y = 0
    max = 0
    min = 65535
    for i in range (1,row):
        for j in range (1,column):
            if( filtered[i,j] != 0 and filtered[i-1,j] == 0):#izq
                if ( j > max):
                    max = j
            if( filtered[i,j] == 0 and filtered[i-1,j] != 0):#derecha
                if ( j < min):
                    print("min")
                    min = j      
            if( filtered[i,j] != 0 and filtered[i,j-1] == 0):#arriba
                if ( i > max):
                    max = i
    filtered[:,min]=65535
    filtered[:,max]=65535
    showImageFiltered(filtered,frame)


    