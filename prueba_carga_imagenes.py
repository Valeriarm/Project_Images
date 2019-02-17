import pydicom 
import numpy as np
import os

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


# obtiene la primera imagen
RefDs = pydicom.dcmread(lstFilesDCM[0])

#guardo las filas, las columnas y el largo de la imagen
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
try:
    SliceThickness = float(RefDs.SliceThickness)
    pixelAspectRatio = ( float(RefDs.PixelAspectRatio[0]), float(RefDs.PixelAspectRatio[1]))
except AttributeError:
    SliceThickness = 1.0
    pixelAspectRatio = (0,0)

#se calcula las medidas de los pixeles 
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), SliceThickness)
pixelSpacing = float(RefDs.PixelSpacing[0]) / float(RefDs.PixelSpacing[1])
areaPixelSpacing = float(RefDs.PixelSpacing[0])*float(RefDs.PixelSpacing[1])

#Show header's caracteristics 
print("Pixel Spacing: " + str(ConstPixelSpacing) + " , " + str(pixelSpacing) + " , area " + str(areaPixelSpacing) + " mm")
print("ID del Paciente: " + RefDs.PatientID)
print("Columnas: " + str(RefDs.Columns))
print("Filas: " + str(RefDs.Rows))
print("Numero de Serie: " + str(RefDs.SeriesNumber))
print("Manufactura: " + str(RefDs.Manufacturer))

