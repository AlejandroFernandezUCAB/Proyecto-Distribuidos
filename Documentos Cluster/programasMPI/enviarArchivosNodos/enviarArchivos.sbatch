#!/bin/bash
#
#SBATCH --partition=all
#SBATCH --job-name=chksum_local
#SBATCH --time=04:00
#SBATCH --output=EnvioArchivos.%j.out
#SBATCH --ntasks=2
#

export IN_FILE=./infile
export LOCAL_HOME=/local_home/$USER
export WP=$(pwd)

echo $(hostname)": Creando archivo $IN_FILE"
find / -type f 1> $IN_FILE

echo $(hostname)": Tansfiriendo archivo $WP/infile a $LOCAL_HOME en los nodos $SLURM_NODELIST"
PDSH_SSH_ARGS_APPEND="-o StrictHostKeyChecking=no" pdsh -w $SLURM_NODELIST cp $WP/infile $LOCAL_HOME
