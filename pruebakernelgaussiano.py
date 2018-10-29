
#librerias
from matplotlib import pyplot as plt
from skimage import io
import numpy as np
#main
#kernel de 3x3
#kerne = np.ones((3,3)) #filtro mediana - promedio
#l = 1.0/9.0

#kernel gaussiano 7x7
kerne = np.array([[0.000036,0.000363,0.001446,0.002291,0.001446,0.000363,0.000036],
                [0.000363,0.003676,0.014662,0.023226,0.014662,0.003676,0.000363],
                [0.001446,0.014662,0.058488,0.092651,0.058488,0.014662,0.001446],
                [0.002291,0.023226,0.092651,0.146768,0.092651,0.023226,0.002291],
                [0.001446,0.014662,0.058488,0.092651,0.058488,0.014662,0.001446],
                [0.000363,0.003676,0.014662,0.023226,0.014662,0.003676,0.000363],
                [0.000036,0.000363,0.001446,0.002291,0.001446,0.000363,0.000036]])
l=1

#kernel gaussiano 3x3
"""
kerne = np.array([[0.110533,0.111399,0.110533],
                [0.111399,0.112271,0.111399],
                [0.110533,0.111399,0.110533]])
l=1
"""
vecinos=3 #cantidad de vecinos
#leer imagen
original = io.imread("lena_gray.png")
"""
#duplicando fila y columna
rowO, columnO = original.shape
image = np.zeros((rowO+n,columnO+n))
row, column = image.shape
for i in range(0,rowO): #recorre el tamaño de la original max:511
    image[0,i+1]=original[0,i]
    image[i+1,0]=original[i,0]
    #faltan dos
for i in range(0,row-2):
    for j in range(0,column-2):
        image[i+1,j+1]=original[i,j]
"""
rowO, columnO=original.shape
#adiciona fila o columna a cada extremo y copia su valor correspondiente.
image = np.pad(original,vecinos,'symmetric')
row, column = image.shape

#nueva imagen
nueva = np.zeros((rowO,columnO))
m = 0
n = 0
for i in range (vecinos,row-vecinos):
    for j in range (vecinos,column-vecinos):
        firsti = i - vecinos
        firstj = j - vecinos  
        endi = i + vecinos + 1
        endj = j + vecinos + 1
        print(str(firsti)+str(firstj)+str(endi)+str(endj)+"neighbors"+str(vecinos))
        nueva [m,n] = np.sum(image[firsti:endi,firstj:endj] * kerne[:,:])
        n=n+1
        """
        #se puede escribir mejor este es solo para 3x3
        nueva[i,j] =((image[i-1,j-1]*kerne[0,0])+(image[i,j-1]*kerne[0,1])+(image[i+1,j-1]*kerne[0,2])+
                    (image[i-1,j]*kerne[1,0])+(image[i,j]*kerne[1,1])+(image[i+1,j]*kerne[1,2])+
                    (image[i-1,j+1]*kerne[2,0])+(image[i,j+1]*kerne[2,1])+(image[i+1,j+1]*kerne[2,2]))*l
        #nueva[i,j]=image[i,j]
        """
    n=0
    m=m+1

plt.imshow(nueva,cmap=plt.cm.gray)

#\:v/
plt.show()