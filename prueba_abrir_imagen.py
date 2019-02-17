import tkinter as tk
import pydicom 
import numpy as np
import os
from matplotlib import pyplot as plt

#
image = os.path.join("C:/Users/Asus/Documents/Procesamiento/MRI Images/","MRI17.dcm")
RefDs = pydicom.dcmread(image)

plt.figure(dpi=300)
plt.axes().set_aspect('equal')

def mostrar():
	plt.imshow(RefDs.pixel_array, cmap=plt.cm.bone) 
	plt.show()

print(RefDs.dir("path"))

##GUI
root = tk.Tk()
titulo = tk.Label(root, text="Image")    
boton = tk.Button(root, text="Mostrar imagen",command=mostrar)


boton.pack()
titulo.pack()


root.mainloop()