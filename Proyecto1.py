from mpi4py import MPI
import time
import random

# -*- coding: utf-8 -()
mapa = {}
# diccionario que tiene las palabras y sus definiciones
diccionario = {}

PATH_LIBRO = 'libro_medicina.txt'
PATH_DICCIONARIO = 'palabras_libro_medicina.txt'

# ----- /Variables Globales ------

# ----- Funciones Para Leer, Contar y Modificar ------

# lee el archivo PATH_DICCIONARIO
def cargarDiccionario():
    with open(PATH_DICCIONARIO,'r') as diccionario_palabras:
        for line in diccionario_palabras:
            splitUpLine = line.split(" ",1)

            palabra = splitUpLine[0]
            definicion = splitUpLine[1]
            # if(mapa.has_key(palabra)):
            #     print palabra, " esta repetida"
            # else:
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

    # si eres el coordinador
    if rank == size-1:
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
        
        # nodos = size 

        chunksize = int(round(len(palabras)/float(size)))
        print "palabras por nodo: {}".format(chunksize)
        # workload = []
        messagesSent = []
        print "Nodo Coordinador envia palabras, de manera asincona"
        for i in range(size-1):
            # Envio a todos los Trabajadores
	        if i < size-2:
	            temp = palabras[chunksize*i:chunksize*(1+i):]
                print "coordinador --> voy a enviar: ",len(temp)," a proceso ",i, ". (",chunksize*i,",",chunksize*(1+i),")"
                # ENVIO SINCRONO F U N C I O N A
                messagesSent.append(comm.isend(temp,dest=i,tag=99))
                # Envio a ultimo trabajador
            elif i == size-2:
                temp = palabras[chunksize*i::]
                print "coordinador --> voy a enviar: ",len(temp)," a proceso ",i, ". (",chunksize*i,",",chunksize*(1+i),")"
		        messagesSent.append(comm.send(temp,dest=i, tag=99))
	            #comm.send("hola soy tu padre", dest=i, tag=99)
		        # print "enviando asincrono a ",i
	
        print "coordinador termino envio asincrono"
	
	
        iMensajes = []
        
        print "Nodo coordinador espera respuesta de manera asincrona"
        for i in range(size):
            req = comm.irecv(source=i, tag=100)
            iMensajes.append(req)
        
        contador = 0
        nodo = 0
        while True:
            if contador == size-1:
                break
            if not iMensajes[nodo].Get_status():
                time.sleep(0.2)
	        # print "espero a ",nodo
            else:
            temp = iMensajes[nodo].wait()
                if temp != None:
                    print "coordinador -> recibi: ",temp,". De nodo: ",nodo
                    contador += 1
	        nodo = (nodo+1)%size
        print "coordinador -> sali del ciclo"
	
    # si eres trabajador
    else:
        diccionario = comm.recv(source=size-1, tag=99)
        print "Diccionario posee esto:" + str(diccionario)
	    # req = comm.irecv(source=size-1, tag=99)
    	# data = req.wait()
        
        print "Nodo",rank," --> recibi: ",len(diccionario)
        # time.sleep(random.randint(1,(rank//3)+2))
        comm.send('Exito!', dest=size-1, tag=100)

        # F A S E  1
        # 1 - Recibir las palabras
        # NO IMPLEMENTADO
        # 2 - Buscar palabras y contarlas (adicionalmente se guarda la posicion de la primera linea)
        lineas_libro = []

        try:
            with open(PATH_LIBRO,'r') as libro:
                # convertimos las lineas del libro en una lista de lineas
                lineas_libro = libro.readlines()
                print ('El libro tiene {} Lineas.\nBuscando palabras y generando mapa de incidencias...'.format( str(len(lineas_libro)) ))

                for idx, linea in enumerate(lineas_libro):
                    # print(idx)
                    contarPalabras(linea.lower(), idx) # convertimos todas las palabras a minusculas...

                #imprimir cantidad de palabras
                print ( '\nProceso ' + str(rank) + ' leyo :\n'+ str(mapa))

        except:
            print('Hubo un error leyendo el libro')
            exit()


if __name__ == '__main__':
    main()
