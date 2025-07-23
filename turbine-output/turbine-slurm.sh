#!/bin/bash
# We changed the M4 comment to d-n-l, not hash
# We may need 'bash -l' for the module system

# Copyright 2013 University of Chicago and Argonne National Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

# TURBINE-SLURM.SH

# Created: esyscmd(date "+%Y-%m-%d %H:%M:%S")

#SBATCH --output=/gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/experiments/ETSC/output.txt
#SBATCH --error=/gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/experiments/ETSC/output.txt

#SBATCH --qos=gp_bscls


#SBATCH --account=bsc08


#SBATCH --job-name=ETSC_job

#SBATCH --time=06:00:00
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=24
#SBATCH -D /gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/experiments/ETSC

# M4 conditional to optionally perform user email notifications


# This block should be here, after other arguments to #SBATCH, so that the user can overwrite automatically set values such as --nodes (which is set in run-init.zsh using PROCS / PPN)
# Note this works because sbatch ignores all but the last of duplicate arguments
# TURBINE_SBATCH_ARGS could include --exclusive, --constraint=..., etc.


# BEGIN TURBINE_DIRECTIVE

# END TURBINE_DIRECTIVE

START=$( date "+%s.%N" )
echo "TURBINE-SLURM.SH START: $( date '+%Y-%m-%d %H:%M:%S' )"

export TURBINE_HOME=$( cd "$(dirname "$0")/../../.." ; /bin/pwd )

VERBOSE=
if (( ${VERBOSE} ))
then
 set -x
fi

TURBINE_PILOT=${TURBINE_PILOT:-}
if (( ! ${#TURBINE_PILOT} ))
then
  TURBINE_HOME=/apps/GPP/SWIFTT/1.6.2-python-3.12.1/turbine
  source ${TURBINE_HOME}/scripts/turbine-config.sh
fi

COMMAND="/usr/bin/tclsh8.6 /gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/experiments/ETSC/swift-t-swift_run_sweep.9CA.tic ETSC data/combinations.jsonl -exe=/gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/experiments/ETSC/COVID19 -settings=/gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/experiments/ETSC/tester.xml -parameters=/gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/experiments/ETSC/combinations.jsonl"

# SLURM exports all environment variables to the job by default
# Evaluate any user turbine -e K=V settings here
ENV_PAIRS=( PROJECT='bsc08' QUEUE='gp_bscls' WALLTIME='06:00:00' TURBINE_OUTPUT='/gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/experiments/ETSC' TURBINE_JOBNAME='ETSC_job' TCLLIBPATH='/apps/GPP/SWIFTT/1.6.2-python-3.12.1/turbine/lib' ADLB_SERVERS='1' TURBINE_WORKERS='767' TURBINE_LOG='1' TURBINE_DEBUG='1' ADLB_DEBUG='1' ADLB_TRACE='0' PATH='/apps/GPP/SWIFTT/1.6.2-python-3.12.1/stc/bin:/apps/GPP/SWIFTT/1.6.2-python-3.12.1/turbine/bin:/apps/GPP/R/4.3.2/INTEL/bin:/apps/GPP/PYTHON/3.12.1/INTEL/bin:/apps/GPP/SQLITE3/3.45.2/INTEL/bin:/apps/GPP/HDF5/1.14.1-2/INTEL/IMPI/bin:/apps/GPP/ANT/1.10.14/bin:/apps/GPP/JDK/8u131/bin:/apps/GPP/ZSH/5.9/GCC/bin:/apps/GPP/SWIG/4.2.1/INTEL/bin:/gpfs/apps/MN5/GPP/ONEAPI/2023.2.0/mpi/2021.10.0/libfabric/bin:/gpfs/apps/MN5/GPP/ONEAPI/2023.2.0/mpi/2021.10.0/bin:/gpfs/apps/MN5/GPP/ONEAPI/2023.2.0/compiler/latest/linux/bin:/gpfs/apps/MN5/GPP/ONEAPI/2023.2.0/compiler/latest/linux/bin/intel64:/apps/ACC/ANACONDA/2023.07/bin:/apps/ACC/ANACONDA/2023.07/condabin:/home/bsc/bsc008602/.local/bin:/home/bsc/bsc008602/bin:/apps/modules/bsc/bin:/apps/GPP/UCX/1.15.0/INTEL/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin' PYTHONPATH='/apps/GPP/SWIFTT/1.6.2-python-3.12.1/turbine/py:/gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/python'  )
for P in "${ENV_PAIRS[@]}"
do
    export "$P"
done

# Use this on Midway:
# module load openmpi gcc/4.9
# Use mpiexec on Midway

# Use this on Bebop:
# module unload intel-mpi
# module unload intel-mkl
# module load gcc/7.1.0
# module load mvapich2
# module list
# TURBINE_LAUNCHER=srun

# Use this on Stampede2
#  TURBINE_LAUNCHER=ibrun

# Use this on Cori:
# TURBINE_LAUNCHER=srun
# module swap PrgEnv-intel PrgEnv-gnu
# module load gcc

TURBINE_LAUNCHER="srun"
TURBINE_INTERPOSER=""

# BEGIN TURBINE_PRELAUNCH

# END TURBINE_PRELAUNCH

if [[ ${TURBINE_LAUNCHER} == 0 ]]
then
  TURBINE_LAUNCHER=srun
fi

# Report modules to output.txt for debugging:
module list

(
  export PMI_MMAP_SYNC_WAIT_TIME=1800
  # Report the environment to a sorted file for debugging:
  printenv -0 | sort -z | tr '\0' '\n' > turbine-env.txt

  set -x
  ${TURBINE_LAUNCHER}  \
                      ${TURBINE_INTERPOSER} \
                      ${COMMAND}
)
CODE=$?

STOP=$( date "+%s.%N" )
# Bash cannot do floating point arithmetic:
DURATION=$( awk -v START=${START} -v STOP=${STOP} \
            'BEGIN { printf "%.3f\n", STOP-START }' < /dev/null )

echo
echo "MPIEXEC TIME: ${DURATION}"
echo "EXIT CODE: ${CODE}"
echo "COMPLETE: $( date '+%Y-%m-%d %H:%M:%S' )"

# Return exit code from launcher
exit ${CODE}

# Local Variables:
# mode: m4;
# End:
