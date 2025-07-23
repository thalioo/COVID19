#!/bin/bash
#SBATCH --job-name "test"
#SBATCH -o output.txt
#SBATCH -e errors.txt
#SBATCH --ntasks 32
#SBATCH --cpus-per-task=56
#SBATCH --time=02:00:00
#SBATCH --qos=gp_bscls
#SBATCH --account=bsc08

#Greasy log files
#######################################################################
export GREASY_LOGFILE=logfile.log

#######################################################################
# Run greasy
#######################################################################

module load greasy
module load python

greasy tasks_complete.txt