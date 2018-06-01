#!/bin/bash
#SBATCH --partition=all 
#SBATCH --job-name=prueba_py
#SBATCH --time=01:00
#SBATCH --output=Prueba.%j.out
#SBATCH --ntasks=11

echo $SLURM_NODELIST

