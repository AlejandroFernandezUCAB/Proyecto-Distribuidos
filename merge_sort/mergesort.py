#!/usr/bin/python

#Funcion para abrir,leer los archivos y todas las palabras
#y pasarlas a un array para luego proceder a  ordenarlas
def abrirArchivo( nombreArchivo):
    
    archivo = open(nombreArchivo, "r")
    palabras = archivo.readlines()
    palabras.sort()
    return palabras


#Main
if __name__ == '__main__':

    archivo1 = abrirArchivo("archivo1")
    archivo2 = abrirArchivo("archivo2")
