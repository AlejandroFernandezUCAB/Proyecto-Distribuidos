from mpi4py import MPI
import time
import random
import sys

# -*- coding: utf-8 -()
mapa = {}
# diccionario que tiene las palabras y sus definiciones
diccionario = {}

PATH_LIBRO = 'libro_medicina.txt'
PATH_DICCIONARIO = 'palabras_libro_medicina.txt'

# ----- /Variables Globales ------

# ----- Funciones Para Leer, Contar y Modificar ------

#Funcion para pasar las palabras del diccionario al mapa

# recibe el diccionario que posee el esclavo
def inicializarMapa( diccionarioE ):

    for palabra in diccionarioE.keys():
        mapa[palabra] = [0, None]
    #print "Hola, soy el MAPA=" + str(mapa)

# recibe: linea del libro y su indice respectivo
# devuleve: un diccionario que tiene la siguiente composicion:
def contarPalabras(linea, indice):
    # A D V E R T E C I A
    # ---------------------
    # la siguiente linea es un fume
    # tarde como media hora para resolverlo
    # muy bonito python...
    # pero una cagada el manejo de caracteres ;)
    #	Linea para version aterir de libr ---> linea = linea.decode('cp1252').encode('utf-8')
    # explicacion:
        # para obtener el archivo txt use adobe reader para convertir el PDF
        # al parecer el programa utiliza esa codificacion de caracteres por vainas de windows
        # https://marketing.adobe.com/resources/help/en_US/whitepapers/multibyte/multibyte_windows1252.html
        # https://stackoverflow.com/questions/12468179/unicodedecodeerror-utf8-codec-cant-decode-byte-0x9c?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    
    # print ('\nlinea: {}'.format(linea))
    # time.sleep(0.8)
    # iteramos las llaves del mapa previamente creado
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
        
        


        palabras = len(diccionario)
        print "Numero de palabras: {}".format(palabras)
        
        


        # nodos = size 

        chunksize = int(round(palabras/float(size)))
        print "palabras por nodo: {}".format(chunksize)
        # workload = []
        messagesSent = []
        print "Proceso Coordinador envia palabras, de manera asincona"
        for i in range(size-1):
            # Envio a todos los Trabajadores
            if i < size-2:
                temp = {element:diccionario[element] for idx,element in enumerate(diccionario) if (idx)>=chunksize*i and (idx)<chunksize*(1+i)}
                #temp = palabras[chunksize*i:chunksize*(1+i):]
                
                print "coordinador --> voy a enviar: ",len(temp)," a proceso ",i, ". (",chunksize*i,",",chunksize*(1+i),")"
                # ENVIO SINCRONO F U N C I O N A
                messagesSent.append(comm.isend(temp,dest=i,tag=99))
                # Envio a ultimo trabajador
            elif i == size-2:
                # temp = palabras[chunksize*i::]
                temp = {element:diccionario[element] for idx,element in enumerate(diccionario) if (idx)>=chunksize*i and (idx)<=len(diccionario)}
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
                # time.sleep(0.1)
	        # print "espero a ",nodo
                pass
            else:
                temp = iMensajes[nodo].wait()
                if temp != None:
                    print "coordinador -> recibi: ",temp,". De Proceso: ",nodo
                    contador += 1
	        nodo = (nodo+1)%size
        print "coordinador -> sali del ciclo"
	
    # si eres trabajador
    else:
        data = dict(comm.recv(source=size-1, tag=99))
        
        print "Proceso",rank," --> recibi: ",len(data)
        
        # time.sleep(random.randint(1,(rank//3)+2))
<<<<<<< HEAD
        
=======
        comm.send('Exito!', dest=size-1, tag=100)
>>>>>>> 92b24c541afd5548cc36912a80e524f6e95f2ac3
        diccionarioE = data 
        inicializarMapa( diccionarioE )
        lineas_libro = []
        
        try:
            with open(PATH_LIBRO,'r') as libro:
                # convertimos las lineas del libro en una lista de lineas
                lineas_libro = libro.readlines()
                print ('Proceso {} ---> Buscando palabras y generando mapa de incidencias...'.format( str(rank) ))

                for idx, linea in enumerate(lineas_libro):
                    # print(idx)
                    contarPalabras(linea.lower(), idx) # convertimos todas las palabras a minusculas...
                #imprimir cantidad de palabras
                print ( '\n\nProceso ' + str(rank) + ' leyo :\n'+ str(mapa)+"\n\n")
                
        except:
            print('Hubo un error leyendo el libro: {}'.format(sys.exc_info()[0]))
            exit()
        
<<<<<<< HEAD
        comm.send('Exito!', dest=size-1, tag=100)
=======
>>>>>>> 92b24c541afd5548cc36912a80e524f6e95f2ac3

if __name__ == '__main__':
    main()
