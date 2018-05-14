import math
# -*- coding: utf-8 -()
mapa = {}
# diccionario que tiene las palabras y sus definiciones
diccionario = {}

PATH_LIBRO = 'libro_medicina.txt'
PATH_DICCIONARIO = 'palabras_libro_medicina.txt'

# ----- /Variables Globales ------

# ----- Funciones Para Leer, Contar y Modificar ------

# lee el archivo PATH_DICCIONARIO
# inicializa el mapa de palabras
def cargarDiccionario():
    with open(PATH_DICCIONARIO,'r') as diccionario_palabras:
        palabras_diccionario = diccionario_palabras.readlines()
        for palabra_definicion in palabras_diccionario:
            temp = palabra_definicion.split(' "')
            palabra = temp[0]
            definicion = temp[1]
            mapa[palabra] = [0, None]
            diccionario[palabra] = limpiarString(definicion)

# # elimina los saltos de linea
def limpiarString(linea):
    return linea.replace("\n","").replace('"',"")

# source: https://stackoverflow.com/questions/761804/how-do-i-trim-whitespace-from-a-python-string
# def strip_one_space(s):
#     if s.endswith(" "): s = s[:-1]
#     if s.startswith(" "): s = s[1:]
#     return s

def main():
    # CARGAR LISTA DE PALABRAS EN MEMORIA
    cargarDiccionario()
    # print((mapa))
    # print ""
    # print((diccionario))
    #
    
    #SCATTER A LOS NODOS
    # picamos el arreglo
    palabras = diccionario.keys()
    print "Numero de palabras: {}".format(len(palabras))
    
    nodos = 4 # = rank

    chunksize = int(math.ceil(len(palabras)/float(nodos)))

    workload = []

    for i in range(nodos):
        workload.append(palabras[chunksize*i:chunksize*(1+i):])

    print workload

if __name__ == '__main__':
    main()