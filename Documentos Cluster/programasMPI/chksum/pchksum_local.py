
#!/usr/bin/env python
"""
Crecion de archivo checksum en sha512 para todo un directorio
en paralelo.
"""

import sys
import hashlib
import os
from mpi4py import MPI

BUF_SIZE = 65536

def get_chksums(file_name):
    md5 = hashlib.md5()
    sha1 = hashlib.sha512()
    with open(file_name, 'rb') as file_d:
        while True:
            data = file_d.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
    
    file_d.close()
    return [md5.hexdigest(), sha1.hexdigest()]

def cal_begin(file_name, rank, size):
    desc = open(file_name, 'r')
    count_lines = len(desc.readlines())
    desc.close()
    
    wload = count_lines / size
    begin = rank * wload
    rest = count_lines % size
    
    return [begin, wload, rest]
    
    
    

if __name__ == '__main__':
    os.chdir(os.environ['LOCAL_HOME'])
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    begin, wload, rest = cal_begin(sys.argv[1], rank, size)
    end = begin + wload
    
    with open(sys.argv[1], 'r+') as file_d:
        walk = 0
        #Saltar lineas
        while walk < begin:
            line = file_d.readline()
            walk = walk + 1
        
        md5 = open(sys.argv[2]+".md5." + str(rank), 'w+')
        sha512 = open(sys.argv[2]+".sha512." + str(rank), 'w+')
        
        # proceso de lineas
        while walk < end:
            file_name = file_d.readline().replace('\n','')
            walk = walk + 1
            print("rank " + str(rank) + " line " + str(walk) + ": " + file_name)
            hashs = get_chksums(file_name)
            md5.write(hashs[0] + " " + file_name + "\n")
            sha512.write(hashs[1] + " " + file_name + "\n")
            
        if rank == size-1 and rest > 0:
            file_name = file_d.readline().replace('\n','')
            while file_name:
                hashs = get_chksums(file_name)
                md5.write(hashs[0] + " " + file_name + "\n")
                sha512.write(hashs[1] + " " + file_name + "\n")
                file_name = file_d.readline().replace('\n','')
            
        md5.close()
        sha512.close()
        
    exit(0)
            
