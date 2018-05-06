#!/usr/bin/python

#Imprimir Archivo ordenado
def imprimirArchivo( imprimir ):
    file = open( "FINAL", "w")
    for x in imprimir:
        file.write( x )
    file.close()

#Funcion para abrir,leer los archivos y todas las palabras
#y pasarlas a un array para luego proceder a  ordenarlas
#Se retorna palabras
def abrirArchivo( nombreArchivo ):

    archivo = open(nombreArchivo, "r")
    palabras = archivo.readlines()
    palabras.sort()
    archivo.close()
    return palabras

#Con esta funcion se va a agarrar el array2 y se agregara a la cola
#Del array1, quedando array1 + arra2 (No es una suma)
#Luego procede a ordenarlo y lo retorno
def agregarPalabrasAOtroArray( array1 , array2 ):
    
    #Agarra el array de segundo lugar y mete elemento por elemento en el array1
    for x in array2:
        if "\n" not in x: 
            x = x + "\n"
            array1.append( x )
        else:
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
    imprimirArchivo( imprimir )

#Pasos:
    # 1. Se procede a abrir el archivo y se retorna en una lista POR LINEA
    # 2. Se abre el siguiente archivo y se retorna de nuevo linea por linea
    # 3. Se agarran las 2 listas anteriores y se ordenan alfabeticamente
    # 4. Se abre un tercer archivo y se retorna linea por linea la lista
    # 5. Se agarra el array ordenado y se le agrega lo dle tercer archivo 
    # 6. Asi sucesivamente hasta terminar de leer los archivos
    # 7. Se imprime el archivo correctamente  
