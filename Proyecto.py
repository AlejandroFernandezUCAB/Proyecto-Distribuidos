#!/usr/bin/env python
# -*- coding: utf-8 -()

from mpi4py import MPI
import numpy
import sys
import random

# ----- Variables Globales ------
# NOTA: se debera leer el archivo de palabras y llenar ambos diccionarios. Esta data es de prueba.
# mapa que tiene las palabras, el numero de incidencias, y las lineas en donde se encuentran
    # mapa['<palabra>'] = [  <numero de incidencias>  ,  <numero de linea de la primera incidencia>]
# (deben estar en minuscula)
mapa = {'regurgitación': [0,None], 'aurícula': [0,None], 'pericarditis': [0,None], 'insuficiencia mitral': [0,None], 'trombosis intraventricular': [0,None]}
# diccionario que tiene las palabras y sus definiciones
diccionario = {'regurgitación': '(regurgitación => Expulsar por la boca,sin vómito,sustancias sólidas o líquidas contenidas en el estómago o en el esófago)' ,
 'aurícula': '(aurícula => Cada una de las dos cavidades superiores del corazón de los anfibios, reptiles, aves y mamíferos, situadas sobre los ventrículos, que reciben la sangre de las venas)', 
 'pericarditis': '(pericarditis => Inflamación del pericardio)', 
 'insuficiencia mitral': '(insuficiencia mitral => Reflujo de sangre ocasionado por la incapacidad de la válvula mitral del corazón de cerrarse firmemente)', 
 'trombosis intraventricular': '( trombosis intraventricular => complicación frecuente en el infarto agudo del miocardio de localización anterior, asociado a discinesia ventricular.)'}

PATH_LIBRO = 'cardiologia.txt'
# ----- /Variables Globales ------

# ----- Funciones Para Leer, Contar y Modificar ------

# recibe: linea del libro y su indice respectivo
# llena constantemente el mapa de palabras
def contarPalabras(linea, indice):
    # A D V E R T E C I A
    # ---------------------
    # la siguiente linea es un fume
    # tarde como media hora para resolverlo
    # muy bonito python...
    # pero una cagada el manejo de caracteres ;)
    linea = linea.decode('cp1252').encode('utf-8')
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


# reemplaza la primera incidencia de la palabra
def reemplazarPrimeraPalabra(lineas_libro):
    # recorremos el mapa
    for palabra in mapa.keys():
        # si se encontro la palabra
        if mapa[palabra][0] != 0:
            # ir a la linea del libro y reemplazar palabra por definicion
                # A D V E R T E C I A  2
                # ---------------------
                # este es un fume un poco mas feo
                # basicamente pasa esto:
                    # leo en codificacion cp1252, codifico a utf-8, reemplazo, decodifico utf-8, codifico en cp1252 para escribir 
            lineas_libro[ mapa[palabra][1] ] = lineas_libro[ mapa[palabra][1] ].decode('cp1252').encode('utf-8').replace(palabra,diccionario[palabra]).decode('utf-8').encode('cp1252')
            # print ('\N-----\NVOY A REEMPLAZAR\NANTES:{}\NDESPUES:{}\N-----\N')

#  ----- /Funciones Para Leer, Contar y Modificar ------



# obtengo todos los nodos del mundo
comm = MPI.COMM_WORLD
# obtengo el rango del nodo actual
rank = comm.Get_rank()
# obtengo el nombre del nodo actual
name = MPI.Get_processor_name()
# obtengo la cantidad de nodos
size = MPI.COMM_WORLD.Get_size()

# si soy el coordinador (n-1)
if rank == size:
    # F A S E  1
    # 1 - Enviar libro y lista de palabras
        # NO IMPLEMENTADO
    # 2 - Recibir palabras ordenadas y sus cantidades, de los trabajadores.
        #     (Recibe de 2 en 2, hace merge sort y luego guarda en archivo temporal local. De 5 a 10 archivos temporales).
        # NO IMPLEMENTADO
    # F A S E  2
    # 1 - Combinar y ordenar las palabras en los archivos temporales con merge sort
        # NO IMPLEMENTADO
    # 2 - Recibir libro modificado por los nodos del anillo
        # NO IMPLEMENTADO


# si soy el trabajador
else:
    # F A S E  1
    # 1 - Recibir libro y palabras
        # NO IMPLEMENTADO
    # 2 - Buscar palabras y contarlas (adicionalmente se guarda la posicion de la primera linea)
    lineas_libro = []
    with open(PATH_LIBRO,'r') as libro:
        # convertimos las lineas del libro en una lista de lineas
        lineas_libro = libro.readlines()

        print ('El libro tiene {} Lineas.\nBuscando palabras y generando mapa de incidencias...'.format( str(len(lineas_libro)) ))

        for idx, linea in enumerate(lineas_libro):
            # print(idx)
            contarPalabras(linea.lower(), idx) # convertimos todas las palabras a minusculas...
        
        #imprimir cantidad de palabras
        print ( '\nProceso ' + str(rank) ' :\n'+ str(mapa))

    # 3 - Ordenar las palabras encontradas
        # NO IMPLEMENTADO
    # 4 - Enviar lista de palabras y sus cantidades al coordinador
        # NO IMPLEMENTADO

    # F A S E  2
    # 1 - si el rango del trabajador es diferente a 0 (x != 0)
    if rank != 0:
        # a - recibe el libro del anterior (Nx-1  -->  Nx)
        # data = comm.recv(source=MPI.ANY_SOURCE, tag=77)
        prev_node = int((rank+size-1)%size)
        libro_modificado = list(comm.recv(source=prev_node,tag=77))
        sys.stdout.write('Proceso %s en %s...Recibiendo de %s... %s\n' % (rank,name,prev_node,str(libro_modificado)) )

        # b - reemplaza la primera incidencia de todas sus palabras
        reemplazarPrimeraPalabra(lineas_libro)
        # escribimos los cambios
        with open('libroModificado.txt','w') as target:
            target.writelines(lineas_libro)

        # c - envia  el libro al siguiente (siguiente = (rango + 1)%TamañoAnillo )
        next_node = int((rank+1)%size)

        sys.stdout.write('Proceso %s en %s -> envia a proceso %s...Enviando %s...\n\
        ' % (rank,name, next_node, str(number2beSent)) )

        comm.send( number2beSent , dest=next_node, tag=77)

    # 2 - si el rango del trabajador es igual a 0 (x == 0)
    else:
        # a - reemplaza la primera incidencia de todas sus palabras
        reemplazarPrimeraPalabra(lineas_libro)
        # escribimos los cambios
        with open('libroModificado.txt.'+str(size),'w') as target:
            target.writelines(lineas_libro)
        # b - envia  el libro al siguiente
        next_node = int((rank+1)%size)

        sys.stdout.write('Proceso %s en %s -> envia a proceso %s...Enviando %s...\n\
        ' % (rank,name, next_node, str(number2beSent)) )

        comm.send( number2beSent , dest=next_node, tag=77)
        # c - recibo el libro del ultimo nodo del anillo, y me bloqueo 
        #     mientras me llega el mensaje del ultimo (IMPORTANTE)
            # NO IMPLEMENTADO
        # d - envio libro modificado por todos los trabajadores a el coordinador
            # NO IMPLEMENTADO




# Proyecto 1 de Sistemas Distribuidos
# 

#  F A S E  1 
#  - - - - - - - - - - -
# hay 2 operaciones en paralelo:
    # operacion Coordinador
        # 1 - Enviar libro y lista de palabras
        # 2 - Recibir palabras ordenadas y sus cantidades, de los trabajadores.
        #     (Recibe de 2 en 2, hace merge sort y luego guarda en archivo temporal local. De 5 a 10 archivos temporales).
    # operacion Trabajador
        # 1 - Recibir libro y palabras
        # 2 - Buscar palabras y contarlas (adicionalmente se guarda la posicion de la primera linea)
        # 3 - Ordenar las palabras encontradas
        # 4 - Enviar lista de palabras y sus cantidades al coordinador

#   F A S E  2
#   - - - - - - - - - - - 
# hay 2 operaciones en paralelo:
    # Operacion Coordinador:
        # 1 - Combinar y ordenar las palabras en los archivos temporales con merge sort
        # 2 - Recibir libro modificado por los nodos del anillo
    # Operacion Trabajador:
        # 1 - si el rango del trabajador es diferente a 0 (x != 0)
            # a - recibe el libro del anterior (Nx-1  -->  Nx)
            # b - reemplaza la primera incidencia de todas sus palabras
            # c - envia  el libro al siguiente (siguiente = (rango + 1)%TamañoAnillo )
        # 2 - si el rango del trabajador es igual a 0 (x == 0)
            # a - reemplaza la primera incidencia de todas sus palabras
            # b - envia  el libro al siguiente
            # c - recibo el libro del ultimo nodo del anillo, y me bloqueo 
            #     mientras me llega el mensaje del ultimo (IMPORTANTE)
            # d - envio libro modificado por todos los trabajadores a el coordinador

