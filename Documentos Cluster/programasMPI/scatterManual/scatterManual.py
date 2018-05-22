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

lista = ['hola', 'mundo', 'como', 'estas']

#Si soy el maestro
if rank == 0:
    for x in xrange(1, size):
        print 'Soy el maestro enviando a ' + str(x)
        comm.send( lista[x-1] , dest=x, tag=1)
else:
    data = comm.recv(source=0, tag=1)
    print data
