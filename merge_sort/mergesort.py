#!/usr/bin/python

#Funcion para abrir,leer los archivos y todas las palabras
#y pasarlas a un array para luego proceder a  ordenarlas
#Se retorna palabras
def abrirArchivo( nombreArchivo ):

    archivo = open(nombreArchivo, "r")
    palabras = archivo.readlines()
    palabras.sort()
    return palabras

#Con esta funcion se va a agarrar el array2 y se agregara a la cola
#Del array1, quedando array1 + arra2 (No es una suma)
#Luego procede a ordenarlo y lo retorno
def agregarPalabrasAOtroArray( array1 , array2 ):
    
    #Agarra el array de segundo lugar y mete elemento por elemento en el array1
    for x in array2:
        array1.append( x )
    array1.sort()
    return array1

#Main
if __name__ == '__main__':

    archivo1 = abrirArchivo("archivo1")
    archivo2 = abrirArchivo("archivo2")
    imprimir = agregarPalabrasAOtroArray( archivo1, archivo2)
    archivo3 = abrirArchivo("archivo3")
    imprimir = agregarPalabrasAOtroArray( imprimir, archivo3)
    archivo4 = abrirArchivo("archivo4")
    imprimir = agregarPalabrasAOtroArray( imprimir, archivo4)
    print imprimir
