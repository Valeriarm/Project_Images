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
    apply = tk.Button(frameTPrepro, text="Aplicar Prepro", command =lambda: applyFilter(frameBR, refDs, filterName.current(),comboBorder.get()))
    uploadKernels(filterName, kernelSize)
    #frameTFilter
    titleTFilter = tk.Label(frameTFilter, text="Filtros")
    filterTFilter = ttk.Combobox(frameTFilter, state="readonly")
    applyF = tk.Button(frameTFilter, text="Aplicar Filtro", command = lambda: wichOne(filterTFilter.get(), comboBorder.get(),frameBR))
    cut = tk.Button(frameTFilter, text="recortar", command = lambda: cutImage(frameBL))
    filterTFilter["values"] =["Sobel","Otsu"]
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
    a.imshow(image, cmap=plt.cm.gray)
    imagesTemp = FigureCanvasTkAgg(f, master=frame)
    imagesTemp.draw()
    imagesTemp.get_tk_widget().pack()

def applyFilter(frame,refDs,kernelNum,borderline):
    global filtered
    if kernelNum == 2:
        newImage = libFilters.median(refDs.pixel_array,1,borderline)
        #ver si si cambio resta de original y filtrada de media
        '''
        r = refDs.pixel_array - newImage
        plt.imshow(r, cmap=plt.cm.gray)
        plt.show()
        '''
        
    else:
        kernel = kernels[kernelNum]
        newImage = libFilters.applyConvolution(refDs.pixel_array,kernel,borderline)
    newImage = newImage.astype(np.int64)#
    #filtered = copy.deepcopy(newImage) 
    filtered = newImage
    showImageFiltered(newImage,frame)

def wichOne (name, borderline,frame):
    if(name == 'Sobel'):
        sobel(borderline,frame)
    elif(name == 'Otsu'):
        otsu(frame)

def sobel(borderline,frame):
    global filtered
    gx = libFilters.applyConvolution(filtered, SOBELX, borderline)
    gy = libFilters.applyConvolution(filtered, SOBELY, borderline)
    g = np.absolute(gx) + np.absolute(gy)
    g = g.astype(np.int64)#
    filtered = np.copy(g)

    showImageFiltered(g,frame)
    

def otsu(frame):
    global filtered
    total = filtered.size
    hist = libFilters.histogram(filtered) #histogram
    #
    nu = 0
    sumB = 0
    wB = 0
    wF = 0
    threshold = 0
    varMax = 0
    for i in range(0,np.amax(filtered)): #imagen 1 brainDicom
        nu += i * hist[i]
    for i in range(0,65000):
        wB += hist[i]
        if (wB == 0):
            continue
        wF = total - wB
        if (wF == 0): 
            break
        sumB += i * hist[i]
        mB = sumB / wB
        mF = (nu - sumB) / wF
        #calculate between class variance
        varBetween = wB * wF * (mB - mF) * (mB - mF)
        if (varMax < varBetween):
            varMax = varBetween
            threshold = i
    print (threshold)
    #threshold divide entre blanco y negro
    row, column = filtered.shape
    for i in range(0,row):
        for j in range(0,column):
            if (filtered[i,j] >= threshold):
                filtered[i,j] = 65353
            elif( filtered[i,j] < threshold):
                filtered[i,j] = 0
    filtered = np.copy(filtered)
    showImageFiltered(filtered,frame)
    '''
    th = filtered.astype(np.int64)#
    hist = libFilters.histogram(th)
    plt.clf()
    plt.plot(th)
    plt.show()
    '''

def cutImage(frame):
    global filtered
    min = 512
    row, column = filtered.shape
    x =0
    y = 0
    max = 0
    min = 65535
    for i in range (1,row):
        for j in range (1,column):
            if( filtered[i,j] == 65353 and filtered[i-1,j] == 0):#izq
                if ( j > max):
                    max = j
            if( filtered[i,j] == 0 and filtered[i-1,j] == 65353):#derecha
                if ( j < min):
                    print("min")
                    min = j
    print(min)
    filtered[:,min]=30000
    filtered[:,max]=30000
    showImageFiltered(filtered,frame)
