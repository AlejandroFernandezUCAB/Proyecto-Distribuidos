#!/usr/bin/python

#Funcion para abrir,leer los archivos y todas las palabras
#y pasarlas a un array para luego proceder a  ordenarlas
def abrirArchivo( nombreArchivo ):

    archivo = open(nombreArchivo, "r")
    palabras = archivo.readlines()
    palabras.sort()
    return palabras

#Con esta funcion se va a agarrar el array2 y se agregara a la cola
#Del array1, quedando array1 + arra2 (No es una suma)
#Luego procede a ordenarlo
def agregarPalabrasAOtroArray( array1 , array2 ):
    for x in array2:
        array1.append( x )
    array1.sort()


#Main
if __name__ == '__main__':

    archivo1 = abrirArchivo("archivo1")
    archivo2 = abrirArchivo("archivo2")
    agregarPalabrasAOtroArray( archivo1, archivo2)
