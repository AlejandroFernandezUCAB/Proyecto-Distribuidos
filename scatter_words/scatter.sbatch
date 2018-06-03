#!/bin/bash
#SBATCH --partition=piv                                           
#SBATCH --job-name=scatter_py
#SBATCH --time=05:00
#SBATCH --output=Scatter.%j.out
#SBATCH --ntasks=8

# nota:
# recordar dejar espacio entre nombre de la funcion y la llave
function initialize {
        echo "----------Preparando el entorno-------------" 
        # limpiamos los modulos del nodo
        module purge
        # cargamos los modulos para correr python
        module load prun gnu7/7.3.0 openmpi3/3.0.0 py2-mpi4py/3.0.0 py2-numpy/1.14.2 py2-scipy/1.0.0
        echo -e "\tModulos cargados..."
        echo -e "----------=====================-------------\n"
}

function runScript {
        # inicializamos el ambiente
        initialize
        echo -e "\n\n---------- Ejecucion de Script de Python -------------"
        time prun python scatterMpi.py 2> error
        echo -e "\n----------=====================-------------\n\n"
}

# --------- main program ----------
runScript
# --------- ============ ----------
