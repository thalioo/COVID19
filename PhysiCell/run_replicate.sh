#!/bin/sh

job_id=`printf "%02d" ${SLURM_PROCID}`

if [ -z "$1" ]
then
    echo ./COVID19 ./output_R${job_id}/config.xml
    exec ./COVID19 ./output_R${job_id}/config.xml
else
    echo ./COVID19 ./$1/output_R${job_id}/config.xml
    exec ./COVID19 ./$1/output_R${job_id}/config.xml
fi
