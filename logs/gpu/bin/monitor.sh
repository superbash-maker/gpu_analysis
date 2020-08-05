#!/bin/bash

LOGROOT=/mnt/lustre/logs/gpu 
HOSTNAME=$(hostname)
LOGDIR=$LOGROOT/${HOSTNAME}
TIMESTAMP=$(date "+%Y%m%d %H:%M"); 
LOGFILE=${LOGDIR}/$TIMESTAMP
GPUCOUNT=$(nvidia-smi -L | wc -l  );

for  ((i=0; i<$GPUCOUNT; i++)); do 
	NVIDIA=$(nvidia-smi -i $i --query-gpu=pci.bus_id,temperature.gpu,utilization.gpu,utilization.memory --format=csv | tr -d " % " | tail -1  )
	PIDS=$(/usr/sbin/lsof -n -w -t /dev/nvidia${i})
	if [ "${PIDS}" != "" ] ; then 
	  PSSTAT=$(ps -o user:20,pgrp,pid,pcpu,pmem,start,time,command -p $PIDS | grep -v ^USER  )
	  USER=$( echo $PSSTAT  | awk '{ print $1 }' )
	  APP=$(basename $(echo $PSSTAT  | awk '{ print $8 }' ) )
	else
	  PSSTAT='null';USER='null';APP='null';PIDS='null'
	fi 
	echo $TIMESTAMP, $HOSTNAME, $i, $NVIDIA, $USER, $APP, $PIDS
done
