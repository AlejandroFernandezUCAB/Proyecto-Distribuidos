#!/bin/bash
#
#SBATCH --partition=all
#SBATCH --job-name=chksum_shared
#SBATCH --time=05:00
#SBATCH --output=chksum_mono.%j.out
#SBATCH --ntasks=1
#

export IN_FILE=./infile

find ./data -type f > $IN_FILE

time python ~/wp/chksum.py $IN_FILE ./outfile_mono

rm $IN_FILE
