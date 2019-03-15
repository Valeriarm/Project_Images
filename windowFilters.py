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

structErosion = s = np.array([[1,1,1],[1,1,1],[1,1,1]])

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
    global filtered
    filters = tk.Toplevel(root)
    #frame
    frameT = tk.Frame(filters,width=250,height=400)
    frameTBorder = tk.Frame(frameT, width=100, height=100,highlightcolor="black", highlightthickness=1)
    frameTPrepro = tk.Frame(frameT, width=100, height=100, highlightcolor="black", highlightthickness=1)
    frameTFilter = tk.Frame(frameT,width=100,height=100, highlightcolor="black", highlightthickness=1)
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
    applyF = tk.Button(frameTFilter, text="Aplicar Filtro", command = lambda: wichOne(filterTFilter.get(),kernelSize.get(),comboBorder.get(),frameBR,filters))
    cut = tk.Button(frameTFilter, text="recortar", command = lambda: cutImage(frameBL))
    filterTFilter["values"] =["Sobel","Otsu", "OtsuParcial","kmeans","erosion","dilatacion", "erosion-dilatacion"]
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
    #button tools
    tools = tk.Button(frameTFilter,text="Herramientas", command=lambda: draw(refDs))
    #pack frameB
    frameB.pack(side='bottom')
    #frameB
    frameBL.pack(side = 'left')
    frameBR.pack(side='left')
    #
    tools.pack(side='bottom')
    #
    showImage(refDs,frameBL)
    showImage(refDs,frameBR)
    filtered = np.copy(refDs)


def draw(matrix):
    plt.imshow(matrix,cmap=plt.cm.gray)
    plt.show()

def showImage(RefDs,frame):
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
    for widget in frame.winfo_children():
        widget.destroy()
    f = plt.Figure()
    a = f.add_subplot(111)
    a.imshow(image, cmap=plt.cm.gray)
    imagesTemp = FigureCanvasTkAgg(f, master=frame)
    imagesTemp.draw()
    imagesTemp.get_tk_widget().pack()

def applyFilter(frame,refDs,kernelNum,kernelSize,borderline):
    global filtered
    if (kernelNum == -1 or kernelSize == "" or borderline == "" ):#no funciona completamente
        tk.messagebox.showinfo("Error", "No se ingreso alguno de los datos necesarios.")
        return    
    elif(kernelNum == 1 or kernelNum == 2 or kernelNum == 3 or kernelNum == 11):#mejorar esta escogencia.
        newImage = libFilters.median(refDs,kernelSize,borderline)
    else:
        kernel = kernels[kernelNum]
        newImage = libFilters.applyConvolution(refDs,kernel,borderline)
    newImage = newImage.astype(np.int64)
    filtered = np.copy(newImage)
    showImageFiltered(newImage,frame)

def argumentsKmeans(filters,name):
    answer = tk.simpledialog.askstring("Entrada", "Numero de centroides",parent=filters)
    centroids = [0]*int(answer)
    tones = [0]*int(answer)
    if int(answer) < 0 or answer is None:
        tk.messagebox.showinfo("Error", "Ingrese el numero de centroides")
        return 
    for i in range(0,int(answer)):
        data = tk.simpledialog.askstring("Entrada", "Centroide numero "+str(i)+":", parent=filters)
        centroids[i] = int(data)
    for j in range(0,int(answer)):
        data = tk.simpledialog.askstring("Entrada", "Tono numero "+str(j)+":", parent=filters)
        tones[j] = int(data)
    return centroids, tones


def wichOne (name,kernelSize,borderline, frame,filters):
    if (kernelSize == "" or borderline == "" or name == ""):
        tk.messagebox.showinfo("Error", "No se ingreso alguno de los datos necesarios.")
        return 
    elif(name == 'Sobel'):
        sobel(borderline,frame)
    elif(name == 'Otsu'):
        applyOtsu(frame)
    elif(name=='OtsuParcial'):
        answer = tk.simpledialog.askstring("Entrada", "Tamaño de la ventana para threshold local..",parent=filters)
        if answer is None:
            tk.messagebox.showinfo("Error", "Ingrese el tamaño de ventana.")
            return
        elif int(answer) < 30 or int(answer) > 512:
            tk.messagebox.showinfo("Error", "Ventana muy grande o pequeña.")
            return
        else:
            applyOtsuParcial(int(answer),frame)
    elif(name=='kmeans'):
        centroids, tones = argumentsKmeans(filters,frame)
        print ("centroids", centroids)
        print("tones", tones)
        applyKmeans(centroids,tones,frame)
    elif ( name  == "erosion"):
        applyErosion(frame)
    elif (name == "dilatacion"):
        applyDilatation(frame)
    elif (name  == "erosion-dilatacion"):
        applyDifference(frame)

        
        
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
    showImageFiltered(filtered,frame)

def applyOtsuParcial(kernelSize,frame):
    global filtered
    filtered = np.copy(libFilters.otsuParcial(filtered, kernelSize))
    print("termino otsu parcial")
    showImageFiltered(filtered,frame)

def applyKmeans(centroids,tones,frame):
    global filtered
    print(centroids)
    stop, pre, newCentroids = libFilters.Kmeans(filtered, centroids)
    while not stop:
        stop, pre, newCentroids = libFilters.Kmeans(filtered,newCentroids)
        print(stop,":",newCentroids)
    print(stop,"ahora a cambiar")
    filtered = np.copy(libFilters.applyGroups(filtered, pre,tones))
    print("termino kmeans")
    showImageFiltered(libFilters.colors(filtered),frame)

def applyErosion(frame):
    global filtered
    global structErosion
    filtered = np.copy(libFilters.erosion(filtered, structErosion))
    showImageFiltered(filtered, frame)

def applyDilatation(frame):
    global filtered
    global structErosion
    filtered = np.copy(libFilters.dilatation(filtered, structErosion))
    showImageFiltered(filtered, frame)

def applyDifference(frame):
    global filtered
    global structErosion
    #erosion menos dilatacion
    erosion = np.copy(libFilters.erosion(filtered, structErosion))
    dilatation = np.copy(libFilters.dilatation(filtered, structErosion))
    filtered = np.copy( dilatation - erosion )
    showImageFiltered(filtered, frame)


def cutImage(frame):
    global filtered
    row, column = filtered.shape
    x = 0
    y = 0
    max = 0
    min = 1
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
    filtered[:,min]=1
    filtered[:,max]=1
    showImageFiltered(filtered,frame)


    
