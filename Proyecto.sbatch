#!/bin/bash
#SBATCH --partition=all                                      
#SBATCH --job-name=proyecto1_py
#SBATCH --time=02:00
#SBATCH --output=Proyecto1.%j.out
#SBATCH --ntasks=21

# nota:
# recordar dejar espacio entre nombre de la funcion y la llave
function enviarLibroYpalabras {
    export LIBRO_MED=libro_medicina.txt
    export PALABRAS=palabras_libro_medicina.txt
    export LOCAL_HOME=/local_home/$USER
    export WP=$(pwd)
    export LAST_NODE=$(python GetLastNode.py $SLURM_NTASKS)
    # echo $(hostname)": Creando archivo $IN_FILE"
    # find / -type f 1> $IN_FILE

    echo $(hostname)": Tansfiriendo archivo $WP/$LIBRO_MED a $LOCAL_HOME/$LIBRO_MED en los nodos $SLURM_NODELIST"
    PDSH_SSH_ARGS_APPEND="-o StrictHostKeyChecking=no" pdsh -w $SLURM_NODELIST cp $WP/$LIBRO_MED $LOCAL_HOME
    echo $(hostname)": Transfiriendo archivo $WP/$LIBRO_MED al coordinador (El Ultimo Proceso)"
    PDSH_SSH_ARGS_APPEND="-o StrictHostKeyChecking=no" pdsh -w beehive-node$LAST_NODE cp $WP/$PALABRAS $LOCAL_HOME
}

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
    time prun python Proyecto1.py 2> error
    echo -e "\n----------=====================-------------\n\n"
}

function limpiarTemporalesNodos {
    PDSH_SSH_ARGS_APPEND="-o StrictHostKeyChecking=no" pdsh -w $SLURM_NODELIST rm $LOCAL_HOME/$LIBRO_MED
    PDSH_SSH_ARGS_APPEND="-o StrictHostKeyChecking=no" pdsh -w beehive-node$LAST_NODE rm $LOCAL_HOME/$PALABRAS
}

# --------- main program ----------
enviarLibroYpalabras
runScript
limpiarTemporalesNodos
# --------- ============ ----------
