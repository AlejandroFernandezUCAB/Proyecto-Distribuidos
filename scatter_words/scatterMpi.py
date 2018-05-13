from mpi4py import MPI
# -*- coding: utf-8 -()
mapa = {}
# diccionario que tiene las palabras y sus definiciones
diccionario = {}

PATH_LIBRO = 'libro_medicina.txt'
PATH_DICCIONARIO = 'palabras.txt'

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
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    if rank == 0:
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
        
        nodos = size - 1 

        chunksize = int(round(len(palabras)/float(nodos)))
	print "palabras por nodo: {}".format(chunksize)
        workload = []

        for i in range(nodos):
	    if i == 0:
                workload.append(None)
	    if i != nodos-1:
                workload.append(palabras[chunksize*i:chunksize*(1+i):])
	    else:
                workload.append(palabras[chunksize*i::])
        #print workload

    else:
        workload = None

    workload = comm.scatter(workload, root=0)
    print '\n- - >  rank',rank,'has workload:',workload,  'Length: '
    if workload != None:
       print len(workload)
    print '\n'

if __name__ == '__main__':
    main()
