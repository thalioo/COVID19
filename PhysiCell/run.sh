#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH -t 00:45:00
#SBATCH -o job_files/with-oxygen-%j.out
#SBATCH -e job_files/with-oxygen-%j.err
#SBATCH --exclusive
#SBATCH --qos=debug

rm -r output_FADD_ko_o2_38/*
./COVID19 config/PhysiCell_settings_FADD_ko_o38.xml
# rm -r output_FADD_ko_sin_o2/*
# ./COVID19 config/PhysiCell_settings_FADD_ko_no_o2.xml

# job_files/no-oxygen-%j.out