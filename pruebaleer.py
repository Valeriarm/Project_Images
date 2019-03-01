import numpy as np

nombre = []
vecinos = []
sigma = []
div = 10

archivo = open("kernel.txt","r")
matrix = ''
for line in archivo.readlines():
    if(line == "*\n"):
        matrix = ''
    elif(line.find("S") != -1):
        words = line.split(" ")
        #la primera es nombre, vecindad y sigma
        nombre.append(words[0])
        vecinos.append(words[1])
        sigma.append(words[2][1:])
        div = float(words[3][:-1])
    else:
        items = line.split("\t")
        items[len(items)-1] = items[len(items)-1][:-1]#elimina el salto de linea
        for i in range(0,len(items)):
            matrix = matrix + items[i] + ' '
        matrix=matrix[:-1]
        matrix = matrix + '; ' 
#convierte la matrix a una numpy array
matrix = matrix[:-2]
fin = np.mat(matrix) * (1/div)
archivo.close()