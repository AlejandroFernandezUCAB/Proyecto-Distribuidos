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

    archivo = open( nombreArchivo , "r")
    palabras = archivo.readlines()
    palabras.sort()
    archivo.close()
    return palabras

#Funcion para agregar elementos de un array a otro
#Esta funcion devuelve el array ya lleno
def agregarElementosArray( arrayDevolver, array):
    
    for x in array:
        if "\n" not in x: 
            x = x + "\n"
            arrayDevolver.append( x )
        else:
            arrayDevolver.append( x )
    
    return arrayDevolver

#Con esta funcion se va a agarrar el array2 y se agregara a la cola
#Del array1, quedando array1 + arra2 (No es una suma)
#Luego procede a ordenarlo y lo retorno
def agregarPalabrasAOtroArray( array1 , array2 ):

    #Inicializando el array donde que se devolvera
    arrayDevolver = []
    #Agarra el arrayDevolver que esta vacio y lo llena con array1
    arrayDevolver = agregarElementosArray( arrayDevolver , array1 )
    #Agarra el arrayDevolver que esta vacio y lo llena con array2
    arrayDevolver = agregarElementosArray( arrayDevolver , array2 )
    #Ordena el array alfabeticamente
    arrayDevolver.sort()
    return arrayDevolver

#Main
if __name__ == '__main__':
    archivo1 = abrirArchivo("archivo1")
    archivo2 = abrirArchivo("archivo2")
    #archivo1 = abrirArchivo("/home/pedro/Documentos/Universidad/Sistemas Distribuidos/ProyectoDistribuidos/merge_sort/archivo1")
    #archivo2 = abrirArchivo("/home/pedro/Documentos/Universidad/Sistemas Distribuidos/ProyectoDistribuidos/merge_sort/archivo2")
    imprimir = agregarPalabrasAOtroArray( archivo1, archivo2)
    #archivo3 = abrirArchivo("/home/pedro/Documentos/Universidad/Sistemas Distribuidos/ProyectoDistribuidos/merge_sort/archivo3")
    archivo3 = abrirArchivo("archivo3")
    imprimir = agregarPalabrasAOtroArray( imprimir, archivo3)
    #archivo4 = abrirArchivo("/home/pedro/Documentos/Universidad/Sistemas Distribuidos/ProyectoDistribuidos/merge_sort/archivo4")
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
