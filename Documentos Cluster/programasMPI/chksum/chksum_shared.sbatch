#!/bin/bash
#
#SBATCH --partition=all
#SBATCH --job-name=chksum_shared
#SBATCH --time=04:00
#SBATCH --output=chksum_shared.%j.out
#SBATCH --ntasks=20
#

export IN_FILE=./infile

find ./data -type f > $IN_FILE

time prun python ~/wp/pchksum.py $IN_FILE ./outfile

cat ./outfile.md5.* > ./outfile.md5
cat ./outfile.sha512.* > ./outfile.sha512

rm ./outfile.md5.*
rm ./outfile.sha512.*
