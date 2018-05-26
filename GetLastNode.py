#!/usr/bin/env python
import math
import sys

def main():
    # Here is an example for quick reference. argv holds the program name at index 0. That's why we start at 1.
    # print command line arguments
    # for arg in sys.argv[1:]:
    #     print arg
    lastRank = int(sys.argv[1])
    print int(math.ceil(lastRank/float(2)))

if __name__ == "__main__":
    main()

# source
# https://www.saltycrane.com/blog/2007/12/how-to-pass-command-line-arguments-to/
