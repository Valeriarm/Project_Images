import tkinter as tk
import pydicom
import numpy as np
import os
from matplotlib import pyplot as plt

image = os.path.join("C:/Users/lalil/Documents/imagenes/MRI/","MRI17.dcm")
RefDs = pydicom.dcmread(image)

plt.figure(dpi=300)
plt.axes().set_aspect('equal')

def showImage():
	plt.imshow(RefDs.pixel_array, cmap=plt.cm.bone)
	plt.show()

##GUI
root = tk.Tk()
titulo = tk.Label(root, text="Image")
boton = tk.Button(root, text="Mostrar imagen",command=showImage)


boton.pack()
titulo.pack()


root.mainloop()