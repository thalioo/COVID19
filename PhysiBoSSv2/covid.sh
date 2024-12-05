#!/bin/bash
#SBATCH --job-name=pb       # Job name
#SBATCH --nodes=1                    # Number of nodes
#SBATCH --ntasks-per-node=1          # Number of tasks per node
#SBATCH --cpus-per-task=48            # Number of CPU cores per task
#SBATCH --time=02:00:00              # Walltime (format: HH:MM:SS)
#SBATCH --output=out.log          # Output log file
#SBATCH --error=err.log            # Error log file
#SBATCH --qos=debug

./COVID19 ./config/set_moi.xml