import tkinter as tk
import pydicom 
import numpy as np
import os
from matplotlib import pyplot as plt

#
image = os.path.join("C:/Users/Asus/Documents/Procesamiento/MRI Images/","MRI22.dcm")
RefDs = pydicom.dcmread(image)

plt.figure(dpi=300)
plt.axes().set_aspect('equal')

def mostrar():
	plt.imshow(RefDs.pixel_array, cmap=plt.cm.bone) 
	plt.show()

#print(RefDs.dir("path"))
#print(RefDs.pixel_array)
#print(len(RefDs.pixel_array))
#print(len(RefDs.pixel_array[0]))

def bordear(image):
	newMatrix=[[0,0,0],[0,0,0],[0,0,0]]
	#print(len(image))
	for i in range (0, len(image)):
		for j in range (0, len(image[0])):
			if (i==0 or i==len(image) or j==0 or j==len(image[0])):
				newMatrix[i][j]=image[i][j]
	
	print(newMatrix)



def bordes(matriz):
	auxMatrix = [[0,0,0],[0,0,0],[0,0,0]]
	l=len(matriz[1])
	l2=len(matriz)-1
	for i in range (l):
		auxMatrix[0][i]=matriz[0][i]
	for i in range (l):
		auxMatrix[l2][i]=matriz[l2][i]
	for i in range (0,l2):
		auxMatrix[i][0]=matriz[i][0]
	for i in range (0,l2):
		auxMatrix[i][l2]=matriz[i][l2]

	#print(auxMatrix)


def convolution(image,kernel):
	#calculo la cantidad de vecinos 
	vecinos=int((len(kernel)-1)/2)
	aux=0
	auxMatrix=[0]*len(image)
	filas=len(image[0])-1
	columnas=len(image)-1
	posVecinos=vecinos-1

	print(vecinos)

	for i in range (len(image)):
		auxMatrix[i] = [0]*len(image[0])

	while (vecinos>aux):
		for i in range (0,len(image)):
			auxMatrix[aux][i]=image[aux][i]
			auxMatrix[i][aux]=image[i][aux]
			auxMatrix[filas-aux][i]=image[filas-aux][i]
			auxMatrix[i][columnas]=image[i][columnas]
		aux=aux+1
			

	#for i in range (vecinos,columnas-vecinos):
	#	for j in range (vecinos, finlas-vecinos):
			
	#print(auxMatrix)

		

		#for i in range ():






##GUI
root = tk.Tk()
titulo = tk.Label(root, text="Image")    
boton = tk.Button(root, text="Mostrar imagen",command=mostrar)


boton.pack()

titulo.pack()

#root.mainloop()


#pruebas
img=[[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]]
k=[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]

print(len(img))
print(len(img[0]))

#convolution(img,k)

mostrar()


