#!/usr/bin/env python
from mpi4py import MPI
import time
import random
import sys
import os

# -*- coding: utf-8 -()
mapa = {}
# diccionario que tiene las palabras y sus definiciones
diccionario = {}
tiempoTranscurridoFase1 = 0 
tiempoTranscurridoFase2 = 0 
PATH_LOCAL = '/local_home/'+os.environ['USER']
PATH_LIBRO = PATH_LOCAL + '/libro_medicina.txt'
PATH_DICCIONARIO = PATH_LOCAL + '/palabras_libro_medicina.txt'

# ----- /Variables Globales ------

# ----- Funciones Para Leer, Contar y Modificar ------
def reemplazarPrimeraPalabra(lineas_libro, diccionarioE):

    # recorremos el mapa
    for palabra in mapa.keys():
        # si se encontro la palabra
        if mapa[palabra][0] != 0:
            lineas_libro[ mapa[palabra][1] ] = lineas_libro[ mapa[palabra][1] ].lower().replace(palabra,diccionarioE[palabra])

def imprimiendoDiccionarioFinal( diccionario ):
    with open('diccionarioFinalizado.txt', 'w') as diccionarioFinal:
        for lineaDiccionario in diccionario:
            diccionarioFinal.writelines( lineaDiccionario.capitalize() + "\n") 

# recibe el diccionario que posee el esclavo
def inicializarMapa( diccionarioE ):

    for palabra in diccionarioE.keys():
        mapa[palabra] = [0, None]
    #print "Hola, soy el MAPA=" + str(mapa)

# recibe: linea del libro y su indice respectivo
# devuleve: un diccionario que tiene la siguiente composicion:
def contarPalabras(linea, indice):
    for palabra in mapa.keys():
        # busca la incidencia de la palabra en toda la linea
        incidencias = linea.count(palabra,0,len(linea))

        if incidencias != 0:

            if mapa[palabra][0] == 0: # si es la primera incidencia
                mapa[palabra][1] = indice  # guardo la linea donde la encontre

            mapa[palabra][0] += incidencias # aumenta la cuenta de la palabra


# lee el archivo PATH_DICCIONARIO
def cargarDiccionario():
    with open(PATH_DICCIONARIO,'r') as diccionario_palabras:
        for line in diccionario_palabras:
            splitUpLine = line.lower().split(" ",1)

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


def extraerYOrdenarPalabrasDeMapa(mapaWorker):
    result = []
    for palabra in mapaWorker.keys():
        auxPalabra = palabra + " "+ str(mapaWorker[palabra][0])
        stringAEnviar = auxPalabra.lower()
        result.append( stringAEnviar )
    result.sort()
    return result

def main( tiempoTranscurridoFase1, tiempoTranscurridoFase2):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    name = MPI.Get_processor_name()

    # si eres el coordinador
    if rank == size-1:
        # CARGAR LISTA DE PALABRAS EN MEMORIA
        cargarDiccionario()
        palabras = len(diccionario)
        print "Numero de palabras: {}".format(palabras)


        chunksize = int(round(palabras/float(size)))
        print "palabras por nodo: {}".format(chunksize)

        messagesSent = []
        print "Proceso Coordinador envia palabras, de manera asincona"
        for i in range(size-1):
            # Envio a todos los Trabajadores
            if i < size-2:
                temp = {element:diccionario[element] for idx,element in enumerate(diccionario) if (idx)>=chunksize*i and (idx)<chunksize*(1+i)}
                print "coordinador --> voy a enviar: ",len(temp)," a proceso ",i, ". (",chunksize*i,",",(chunksize*(1+i))-1,")"
                # ENVIO SINCRONO F U N C I O N A
                messagesSent.append(comm.isend(temp,dest=i,tag=99))
                # Envio a ultimo trabajador
            elif i == size-2:
                # temp = palabras[chunksize*i::]
                temp = {element:diccionario[element] for idx,element in enumerate(diccionario) if (idx)>=chunksize*i and (idx)<=len(diccionario)}
                print "coordinador --> voy a enviar: ",len(temp)," a proceso ",i, ". (",chunksize*i,",",len(diccionario),")"
                messagesSent.append(comm.send(temp,dest=i, tag=99))
	        # print "enviando asincrono a ",i
	
        print "coordinador termino envio asincrono"
	
	
        iMensajes = []
        
        print "Nodo coordinador espera respuesta de manera asincrona"
        for i in range(size):
            req = comm.irecv(source=i, tag=100)
            iMensajes.append(req)
        
        contador = 0
        nodo = 0
        listaDiccionarioC = []
        while True:
            if contador == size-1:
                imprimiendoDiccionarioFinal(listaDiccionarioC)
                break
            if not iMensajes[nodo].Get_status():
                # time.sleep(0.1)
	        # print "espero a ",nodo
                pass
            else:
                temp = iMensajes[nodo].wait()
                if temp != None:
                    print "coordinador -> recibi: ",len(temp)," elementos De Proceso: ",nodo
                    
                    if contador == 0:
                        listaDiccionarioC.extend( temp )
                    else:
                        listaDiccionarioC.extend( temp )
                        listaDiccionarioC.sort()
                        
                    contador += 1
 
	    nodo = (nodo+1)%size
        print "coordinador -> sali del ciclo"

        libro_modificado = list(comm.recv(source = size-2 ,tag=420))

        print "coordinador -> Recibi Libro Modificado...Escribiendo En archivo..."

        # Linea de prueba
        with open('libroModificado RESULTATE.txt','w') as target:
            target.writelines(libro_modificado)
	
    # si eres trabajador
    else:
        data = dict(comm.recv(source=size-1, tag=99))
        
        print "Proceso",rank," --> recibi: ",len(data)
        
        # time.sleep(random.randint(1,(rank//3)+2))
        
        diccionarioE = data 
        inicializarMapa( diccionarioE )
        lineas_libro = []
        
        try:
            with open(PATH_LIBRO,'r') as libro:
                comienzo = time.time()
                # convertimos las lineas del libro en una lista de lineas
                lineas_libro = libro.readlines()
                print ('Proceso {} ---> Buscando palabras y generando mapa de incidencias...'.format( str(rank) ))

                for idx, linea in enumerate(lineas_libro):
                    # print(idx)
                    contarPalabras(linea.lower(), idx) # convertimos todas las palabras a minusculas...
                tiempoTranscurrido = time.time() - comienzo
                tiempoTranscurridoFase1 = tiempoTranscurrido
                tiempoTranscurridoFase1 = round( tiempoTranscurridoFase1, 3)
                print "Soy el proceso:"+ str(rank) + " de la fase 1 y transcurrieron " + str(tiempoTranscurrido) + " segundos ejecutando el proceso del libro"
                #imprimir cantidad de palabras
                #print ( '\n\nProceso ' + str(rank) + ' leyo :\n'+ str(mapa)+"\n\n")
                
        except:
            print('Hubo un error leyendo el libro: {}'.format(sys.exc_info()[0]))
            exit()
        

        listaPalabras = extraerYOrdenarPalabrasDeMapa( mapa )

        comm.isend( listaPalabras , dest=size-1 , tag=100 ) 
        

        # F A S E  2
        # 1 - si el rango del trabajador es diferente a 0 (x != 0)
        if rank != 0:
            # a - recibe el libro del anterior (Nx-1  -->  Nx)
            # data = comm.recv(source=MPI.ANY_SOURCE, tag=77)
            prev_node = int((rank+size-1)%size)
            libro_modificado = list(comm.recv(source=prev_node,tag=77))
            sys.stdout.write('Proceso %s en %s...Recibiendo de %s...\n' % (rank,name,prev_node) )

            # b - reemplaza la primera incidencia de todas sus palabras
            comienzoParte2 = time.time()
            reemplazarPrimeraPalabra(libro_modificado,diccionarioE)     
            tiempoTranscurridoParte2 = time.time() - comienzo
            tiempoTranscurridoFase2 = tiempoTranscurridoParte2
            tiempoTranscurridoFase2 = round( tiempoTranscurridoFase2 , 3)
            print "Soy el proceso:"+ str(rank) + " de la fase 2 y transcurrieron " + str(tiempoTranscurridoParte2) + " segundos ejecutando el proceso del libro"
            # escribimos los cambios
            # c - envia  el libro al siguiente (siguiente = (rango + 1)%TamanoAnillo )
            next_node = int((rank+1)%size)
            if next_node != size-1:
                tag = 77
            else:
                tag = 420
            
            comm.send( libro_modificado , dest=next_node, tag=tag)

        # 2 - si el rango del trabajador es igual a 0 (x == 0)
        else:
            # a - reemplaza la primera incidencia de todas sus palabras
            comienzoParte2 = time.time()
            reemplazarPrimeraPalabra(lineas_libro,diccionarioE)
            tiempoTranscurridoParte2 = time.time() - comienzo
            tiempoTranscurridoFase2 = tiempoTranscurridoParte2
            tiempoTranscurridoFase2 = round( tiempoTranscurridoFase2 , 3)
            # escribimos los cambios
            # b - envia  el libro al siguiente
            next_node = int((rank+1)%size)
            comm.send( lineas_libro , dest=next_node, tag=77)

        #Aqui mando al nodo coordinador los resultados de los tiempos de la fase 1
    if rank == size - 1:
        dataTiempoFase1 = comm.gather( 0 , root = (size -1))
        dataTiempoFase1.remove(0)
        print "Estos son los resultados de la primera fase (Todo presentado en segundos):", dataTiempoFase1
    else:
        dataTiempoFase1 = comm.gather( tiempoTranscurridoFase1 , root = (size -1))

    #Aqui mando al nodo coordinador los resultados de los tiempos de la fase 1
    if rank == size - 1:
        dataTiempoFase2 = comm.gather( 0 , root = (size -1))
        dataTiempoFase2.remove(0)
        print "Estos son los resultados de la primera fase (Todo presentado en segundos):", dataTiempoFase2
    else:
        #Si el tiempo transcurrido no es 0 no lo mandes
        if tiempoTranscurridoFase2 != 0:
            dataTiempoFase2 = comm.gather( tiempoTranscurridoFase2 , root = (size - 1))

if __name__ == '__main__':
    main( tiempoTranscurridoFase1, tiempoTranscurridoFase2)
