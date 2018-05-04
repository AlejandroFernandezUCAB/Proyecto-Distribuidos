#!/usr/bin/env python
"""
Crecion de archivo checksum en sha512 para todo un directorio
"""

import sys
import hashlib


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


if __name__ == '__main__':
    with open(sys.argv[1], 'r+') as file_d:
        md5 = open(sys.argv[2]+".md5", 'w+')
        sha512 = open(sys.argv[2]+".sha512", 'w+')
        file_name = file_d.readline().replace('\n','')
        while file_name:
            hashs = get_chksums(file_name)
            md5.write(hashs[0] + " " + file_name + "\n")
            sha512.write(hashs[1] + " " + file_name + "\n")
            file_name = file_d.readline().replace('\n','')
            
        md5.close()
        sha512.close()
        
    exit(0)
