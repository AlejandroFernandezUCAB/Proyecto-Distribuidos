#!/bin/bash
#SBATCH --partition=piv                                           
#SBATCH --job-name=p2p_message_py
#SBATCH --time=01:00
#SBATCH --output=p2p_message_py.%j.out
#SBATCH --ntasks=8

# nota:
# recordar dejar espacio entre nombre de la funcion y la llave
function initialize {
	echo "----------Preparando el entorno-------------" 
	# limpiamos los modulos del nodo
	module purge
	# cargamos los modulos para correr python
	module load prun gnu7/7.3.0 openmpi3/3.0.0 py2-mpi4py/3.0.0 py2-numpy/1.14.2
	echo -e "\tModulos cargados..."
	echo -e "----------=====================-------------\n"
}

function runScript {
	# inicializamos el ambiente
	initialize

	echo -e "\n\n---------- Ejecucion de Script de Python -------------"
	prun p2pmessage.py 
	echo -e "\n----------=====================-------------\n\n"
}

# --------- main program ----------
runScript
# --------- ============ ----------
