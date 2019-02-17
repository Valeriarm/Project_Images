import tkinter as tk
import pydicom 
import numpy as np
import os

from tkinter.filedialog import askopenfilename
from matplotlib import pyplot as plt


#ubicacion de la imagen
pathDicom = "C:/Users/Asus/Documents/Procesamiento/MRI Images/"
#lista que vamos a llenar con todas las imagenes de la carpeta MRI Images
lstFilesDCM = [] #empty list

#for llena el array lstFilesDCM con las imagenes de la carpeta
#os: es una libreria

for dirName, subdirList, fileList in os.walk(pathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower(): #check dicom 
            lstFilesDCM.append(os.path.join(dirName,filename))
            
#lets check what we have in the list
#print(lstFilesDCM)

# obtiene la primera imagen
RefDs = pydicom.dcmread(lstFilesDCM[0])



tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)