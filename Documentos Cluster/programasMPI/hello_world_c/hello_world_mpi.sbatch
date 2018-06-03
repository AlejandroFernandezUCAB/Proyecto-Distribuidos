#!/bin/bash
#
#SBATCH --partition=piv
#SBATCH --job-name=hello_world_c
#SBATCH --time=10:00
#SBATCH --output=hello_world_c.%j.out
#SBATCH --ntasks=4
#

echo "-------Inicio de Proceso en mpi------"
prun ~/bin/hello_world_c
echo "-------Fin de Proceso en mpi------"
