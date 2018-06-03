#!/bin/bash
#
#SBATCH --partition=all
#SBATCH --job-name=chksum_local
#SBATCH --time=04:00
#SBATCH --output=chksum_local.%j.out
#SBATCH --ntasks=20
#

export IN_FILE=./infile
export LOCAL_HOME=/local_home/$USER
export WP=$(pwd)

echo $(hostname)": Creando archivo $IN_FILE"
find ./data -type f > $IN_FILE

echo $(hostname)": Tansfiriendo archivo $WP/infile a $LOCAL_HOME en los nodos $SLURM_NODELIST"
pdsh -w $SLURM_NODELIST cp $WP/infile $LOCAL_HOME
echo $(hostname)": Synconizando directorios $WP/data a $LOCAL_HOME/data en los nodos $SLURM_NODELIST"
pdsh -w $SLURM_NODELIST rsync -a $WP/data $LOCAL_HOME

echo $(hostname)": Ejecutando el programa en Paralelo"
time prun python ~/wp/pchksum_local.py ./infile ./outfile

echo $(hostname)": Tansfiriendo archivos $LOCAL_HOME/outfile* a $WP en los nodos $SLURM_NODELIST"
pdsh -w $SLURM_NODELIST mv $LOCAL_HOME/outfile\* $WP/
echo $(hostname)": Eliminando archivos en los nodos $SLURM_NODELIST"
pdsh -w $SLURM_NODELIST rm $LOCAL_HOME/infile

echo $(hostname)": Preparando archivos finales."
cat ./outfile.md5.* > ./outfile.md5
cat ./outfile.sha512.* > ./outfile.sha512
rm ./outfile.md5.* ./outfile.sha512.*
rm $IN_FILE
