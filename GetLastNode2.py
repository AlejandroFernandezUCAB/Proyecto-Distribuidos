#!/usr/bin/env python
import math
import sys

def main():
    # Here is an example for quick reference. argv holds the program name at index 0. That's why we start at 1.
    # print command line arguments
    # for arg in sys.argv[1:]:
    #     print arg
    # ejemplo de input: beehive-node[1-3,10-12] 
    slurm_nodelist = str(sys.argv[1])
    lastNode = slurm_nodelist[13:len(slurm_nodelist)-1].split(',')[-1].split('-')[-1]
    print lastNode

if __name__ == "__main__":
    main()

# source
# https://www.saltycrane.com/blog/2007/12/how-to-pass-command-line-arguments-to/
