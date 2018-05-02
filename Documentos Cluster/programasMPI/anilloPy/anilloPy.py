#!/usr/bin/env python

from mpi4py import MPI
import numpy
import sys
import random

# obtengo todos los nodos del mundo
comm = MPI.COMM_WORLD
# obtengo el rango del nodo actual
rank = comm.Get_rank()
# obtengo el nombre del nodo actual
name = MPI.Get_processor_name()
# obtengo la cantidad de nodos
size = MPI.COMM_WORLD.Get_size()

# enviando mensaje alsiguiente
next = int((rank+1)%size)
number2beSent = {'random': random.randint(0,28)}
sys.stdout.write('Proceso %s en %s -> envia a proceso %s...Enviando %s...\n\
' % (rank,name, next, str(number2beSent)) )
comm.send( number2beSent , dest=next, tag=77)

#  Recibiendo mensaje del anterior
# data = comm.recv(source=MPI.ANY_SOURCE, tag=77)
prev = int((rank+size-1)%size)
data = comm.recv(source=prev,tag=77)
sys.stdout.write('Proceso %s en %s...Recibiendo de %s... %s\n' % (rank,name,prev,str(data)) )
