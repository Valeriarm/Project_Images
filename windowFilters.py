import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import libFilters
import tkinter.font as tkFont

sigma = []
kernels = [] #heave
state = []
SOBELX = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

SOBELY = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]]) 
filtered = np.ones((512,512))

color1 = [0,50,0] #verde
color2 = [255,0,0]#rojo
color3 =  [0,0,100]#cyan
color4 = [255,255,255] #blanco
color5 = [0,0,0] #negro
color6 = [255,255,0]#amarillo
color7 = [255,0,255]#rosa
color8 = [255,150,0]#naranja
color =  [color1, color2, color3, color4, color5,color6, color7,color8]

struct = np.array([[1,1,1],[1,1,1],[1,1,1]])

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
    #style things
    blueBack = '#%02x%02x%02x' % (1,135,185)
    blueButtons = '#%02x%02x%02x' % (102,184,214)
    bold = tkFont.Font(weight='bold')
    filters.configure(bg=blueBack)
    combostyle= ttk.Style()
    combostyle.theme_create('combostyle',
                            parent='alt',
                            settings = { 'TCombobox': 
                            { 'configure':
                                { 'selectbackground': '#%02x%02x%02x' % (1,135,185),
                                    'fieldbackground': '#%02x%02x%02x' % (102,184,214),
                                    'background': '#%02x%02x%02x' % (102,184,214),
                                    'foreground': '#%02x%02x%02x' % (1,135,185)
                                }}})
    combostyle.theme_use('combostyle')
    #frames
    frameT = tk.Frame(filters,width=250,height=400)
    frameTPrepro = tk.Frame(frameT, width=100, height=100)
    frameTFilter = tk.Frame(frameT,width=100,height=100)
    frameLabeling = tk.Frame(frameT,width=100,height=100)
    frameState = tk.Frame(frameT,width=100,height=100)
    frameMiddle = tk.Frame(filters, width=1278, height=20)
    frameB = tk.Frame(filters,width=250,height=400)
    frameBL = tk.Frame(frameB, width=100, height=400)
    frameBR = tk.Frame(frameB, width=100,height=400)
    #background
    frameT.configure(background=blueBack)
    frameTPrepro.configure(background=blueBack)
    frameTFilter.configure(background=blueBack)
    frameLabeling.configure(background=blueBack)
    frameState.configure(background=blueBack)
    frameMiddle.configure(background=blueButtons)
    #frameTPrepro
    title = tk.Label(frameTPrepro,background=blueBack,fg='white',font=bold, text="PREPROCESAMIENTO")
    numImage = tk.Label(frameTPrepro,background=blueBack,fg='white',text="Imagen numero: "+str(num+1))
    comboBorder = ttk.Combobox(frameTPrepro, state="readonly")
    comboBorder["values"]=["ignorar","reflejados","ceros"]
    filterName = ttk.Combobox(frameTPrepro, state="readonly")
    kernelSize = ttk.Combobox(frameTPrepro, state="readonly")
    apply = tk.Button(frameTPrepro,background=blueButtons,fg='white', text="Aplicar Kernel", command =lambda: applyFilter(appliedFilters, frameBR, refDs, filterName.current(),kernelSize.get(),filterName.get(),comboBorder.get()))
    uploadKernels(filterName, kernelSize)
    #frameTFilter
    titleTFilter = tk.Label(frameTFilter,background=blueBack,fg='white',font=bold, text="SEGMENTACION")
    filterTFilter = ttk.Combobox(frameTFilter, state="readonly")
    applyF = tk.Button(frameTFilter,background=blueButtons,fg='white', text="Aplicar Filtro", command = lambda: wichOne(appliedFilters, filterTFilter.get(),kernelSize.get(),comboBorder.get(),frameBR,filters, separate))
    tools = tk.Button(frameTFilter,background=blueButtons,fg='white',text="Herramientas", command=lambda: draw(filtered))
    #cut = tk.Button(frameTFilter, text="recortar", command = lambda: cutImage(frameBL))
    filterTFilter["values"] =["Sobel","Otsu", "OtsuParcial","kmeans","erosion","dilatacion", "dilatacion-erosion"]
    #frameSeparateLabels
    titleLabel = tk.Label(frameLabeling,background=blueBack,fg='white',font=bold, text="ETIQUETADO")
    separate = ttk.Combobox(frameLabeling, state ='readonly')
    buttonSeparate = tk.Button(frameLabeling,background=blueButtons,fg='white', text="Separar", command=lambda: applyOneColor(separate.current(),frameBR))
    #frame state
    titleAppliedFilters = tk.Label(frameState,background=blueBack,fg='white',font=bold, text="Aplicados")
    appliedFilters = tk.Text(frameState, height=10, width=20)
    appliedFilters.config(state='disabled')
    #pack ############################
    frameT.pack(side='top')
    #frameTPrepro
    frameTPrepro.pack(side='left', padx=5, pady=5)
    title.pack(side='top',padx=5,pady=5)
    numImage.pack(side='top',padx=5,pady=5)
    comboBorder.pack(side='top',padx=5,pady=5)
    filterName.pack(side='top',padx=5,pady=5)
    kernelSize.pack(side='top',padx=5,pady=5)
    apply.pack(side='top',padx=5,pady=5)
    #frameTFilter
    frameTFilter.pack(side='left', padx=5, pady=5)
    titleTFilter.pack(side = 'top', padx=5, pady=5)
    filterTFilter.pack(side='top',padx=5,pady=5)
    applyF.pack(side='top',padx=5,pady=5)
    #cut.pack(padx=5,pady=5)
    tools.pack(side='top',padx=5,pady=5)
    #pack Labeling
    frameLabeling.pack(side = 'left')
    titleLabel.pack(side='top',padx=5,pady=5)
    separate.pack(side='top',padx=5,pady=5)
    buttonSeparate.pack(side='top',padx=5,pady=5)
    #pack state
    frameState.pack(side = 'left')
    titleAppliedFilters.pack(side='top',padx=5,pady=5)
    appliedFilters.pack(side='top',padx=5,pady=5)

    #pack frameB
    frameB.pack(side='bottom')
    #frame middle pack
    frameMiddle.pack(side = 'bottom')
    #frameB
    frameBL.pack(side = 'left')
    frameBR.pack(side='left')
    #charge inicial images
    showImage(refDs,frameBL)
    showImage(refDs,frameBR)
    filtered = np.copy(refDs)

#functions to show images
def draw(matrix):
    plt.imshow(matrix,cmap=plt.cm.gray)
    plt.show()

def showImage(RefDs,frame):
    for widget in frame.winfo_children():
        widget.destroy()
    #crea el elemento que va a contener la imagen
    f = plt.Figure()
    a = f.add_subplot(111)
    a.imshow(RefDs, cmap=plt.cm.gray)#
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

#functions to prepocess the image cleaning the noise

def applyFilter(textState, frame,refDs,kernelNum,kernelSize,filterName,borderline):
    global filtered
    if (kernelNum == -1 or kernelSize == "" or borderline == "" ):
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
    #actualizar estado
    global state
    state = []
    state.append(str(filterName)+' '+str(kernelSize))
    textState.configure(state='normal')
    textState.delete('1.0', 'end')
    textState.insert('end', str(filterName)+' '+str(kernelSize)+'x'+str(kernelSize)+'\n')
    textState.configure(state='disabled')

################

# catch input from user in kmeans
def argumentsKmeans(filters,name):
    try:
        answer = tk.simpledialog.askstring("Entrada", "Numero de centroides",parent=filters)
        centroids = [0]*int(answer)
        tones = [0]*int(answer)
        if int(answer) < 0 or answer is None:
            tk.messagebox.showinfo("Error", "Ingrese el numero de centroides")
            return 
        for i in range(0,int(answer)):
            data = tk.simpledialog.askstring("Entrada", "Centroide numero "+str(i)+":", parent=filters)
            centroids[i] = int(data)
        return centroids
    except:
        tk.messagebox.showinfo("Error", "No se ingreso alguno de los datos necesarios.")
    
################


# call the apropiate filters with the data that needs 
def wichOne (textState, name,kernelSize,borderline, frame,filters,separate):
    start_time = datetime.now()
    if (kernelSize == "" or borderline == "" or name == ""):
        tk.messagebox.showinfo("Error", "No se ingreso alguno de los datos necesarios.")
        return 
    elif(name == 'Sobel'):
        applySobel(borderline,frame)
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
        centroids = argumentsKmeans(filters,frame)
        applyKmeans(centroids,frame,separate)
        name = name + ' C: '+str(len(centroids))
    elif ( name  == "erosion"):
        applyErosion(frame)
    elif (name == "dilatacion"):
        applyDilatation(frame)
    elif (name  == "dilatacion-erosion"):
        applyDifference(frame)
    end_time = datetime.now()
    print(str(name) +" time duration: ", format(end_time - start_time))
    global state
    state.append(str(name))
    textState.configure(state='normal')
    textState.insert('end', str(name)+'\n')
    textState.configure(state='disabled')

####################


def fieldSeparate(separate, newCentroids):
    separate["values"] = []
    colorsName = ["verde","rojo","azul","blanco","negro","amarillo","rosa","naranja"]
    for i in range(0,len(newCentroids)):
        fields = list(separate["values"])
        separate["values"]=fields+[colorsName[i]]

#functions that call the filter 

def applySobel(borderline,frame):
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
    showImageFiltered(filtered,frame)

def applyKmeans(centroids,frame, separate):
    
    global filtered
    stop, pregroups, newCentroids, indexMatrix = libFilters.Kmeans(filtered, centroids)
    while not stop:
        stop, pregroups, newCentroids, indexMatrix = libFilters.Kmeans(filtered,newCentroids)
        print(stop,":",newCentroids)
    filtered = np.copy(libFilters.applyGroups(filtered, pregroups, indexMatrix, newCentroids))
    fieldSeparate(separate, newCentroids)
    print("termino kmeans")
    showImageFiltered(filtered,frame)

def applyErosion(frame):
    global filtered
    global struct
    libFilters.erosion(filtered, struct)
    showImageFiltered(filtered, frame)

def applyDilatation(frame):
    global filtered
    global struct
    filtered = np.copy(libFilters.dilatation(filtered, struct))
    showImageFiltered(filtered, frame)

def applyDifference(frame):
    global filtered
    global struct
    #erosion menos dilatacion
    erosion = np.copy(libFilters.erosion(filtered, struct))
    dilatation = np.copy(libFilters.dilatation(filtered, struct))
    filtered = np.copy( dilatation - erosion )
    showImageFiltered(filtered, frame)

#############################

def applyOneColor(selectedColorIndex,frame):
    global filtered
    background = [0,0,0]
    showImageFiltered(libFilters.showOneColor(filtered,selectedColorIndex),frame)

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





    
