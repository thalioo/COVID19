#!/bin/sh

job_id=`printf "%02d" ${SLURM_PROCID}`

echo ./COVID19 ./output_R${job_id}/config.xml
exec ./COVID19 ./output_R${job_id}/config.xml
