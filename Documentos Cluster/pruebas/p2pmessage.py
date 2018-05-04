#!/usr/bin/env python

from mpi4py import MPI
import numpy
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
name = MPI.Get_processor_name()
size = MPI.COMM_WORLD.Get_size()
if rank == 0:
    data = {'a': 7, 'b': 3.14}
    sys.stdout.write('Hola, soy el proceso %s de %s en el nodo %s\n\
    Enviando el diccionario...%s\n' % (rank,size,name,str(data)) )
    comm.send(data, dest=int(1), tag=int(0)) 
    # sys.stdout.write('data = %s'% (data))
elif rank == 1:
    data = comm.recv(source=0,tag=0)
    sys.stdout.write('Hola, soy el proceso %s de %s en el nodo %s\n\
    Recibiendo el diccionario...\n' % (rank,size,name) )
    sys.stdout.write('data = ' + str(data))
else:
    sys.stdout.write('\n--- = = Nodo: %s, no envia mensajes = = ----\n'% ( name ) )
