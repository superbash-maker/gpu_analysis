#!/bin/bash 

LOGROOT=/mnt/lustre/logs/gpu 
HOSTNAME=$(hostname)
LOGDIR=$LOGROOT/${HOSTNAME}
TIMESTAMP=$(date "+%Y%m%d %H:%M"); 
LOGFILE=${LOGDIR}/$TIMESTAMP
PIDS=$(lsof -n -w -t /dev/nvidia*)
GPUCOUNT=$(nvidia-smi -L | wc -l  );

for  ((i=0; i<$GPUCOUNT; i++)); do 
	NVIDIA=$(nvidia-smi -i $i --query-gpu=pci.bus_id,temperature.gpu,utilization.gpu,utilization.memory --format=csv | tr -d " % " | tail -1  )
#  echo -n  "$TIMESTAMP, $HOSTNAME, $i, $NVIDIA, "
#  if [ "${PIDS}" != "" ] ; then
#  APP=null
#  USER=null
#  MYPID=null
	PIDS=$(lsof -n -w -t /dev/nvidia${i})

#	echo DEBUG: PIDS $PIDS

	#PIDS=$(nvidia-smi -i $i --query-compute-apps=pid --format=csv )
#      for p in $PIDS; do
	if [ "${PIDS}" != "" ] ; then 
	  PSSTAT=$(ps -o user:20,pgrp,pid,pcpu,pmem,start,time,command -p $PIDS | grep -v ^USER  )

#	  echo DEBUG $PSSTAT
	  MYPID=000000
	  MYPID=$( echo $PSSTAT  | awk '{ print $3 }' )
	  USER=$( ps aux | grep $MYPID  | awk '{ print $1 }')
#	  USER=$( echo $PSSTAT  | awk '{ print $1 }' )
	  APP=$(basename $(echo $PSSTAT  | awk '{ print $8 }' ) )
	  if [ "${UPID}" != "" ]; then 
		  UNAME=$( ps aux | grep ${UPID}   | awk '{ print $1 }' )
	  else
		  UNAME=null
	  fi

	  GPUPID=$(lsof -n -w -t /dev/nvidia$i)

	else
	  PSSTAT='null';USER='null';APP='null';PIDS='null'
	fi 

#	UPID=$(nvidia-smi -i $i --query-compute-apps=pid --format=csv | grep -v pid )

#	echo "============= Debug: ", UPID=$UPID
#        if [ "${UPID}" != "" ]; then 	
#		for u in $UPID; do 
#		  UNAME=$(ps aux | grep $u | grep -v root | awk '{print $1 }')
#		  echo  DEBUG  $USER, $APP, "GPUpid= ", $GPUPID, "uname= "  $UNAME
#		  echo $TIMESTAMP, $HOSTNAME, $i, $NVIDIA, $UNAME, $APP, $u
#		done
#	else
#		  UNAME=null; APP=null; GPUPID=null
#	fi 
#	UNAME=$( ps aux | grep $UPID   | awk '{ print $1 }' )

	echo $TIMESTAMP, $HOSTNAME, $i, $NVIDIA, $USER, $APP, $MYPID, $GPUPID


	#echo "DEBUG ;===>" $p ${MYPID} 
        #  if [ "$p" == "${MYPID}" ] ; then 
#  echo "====>"  $TIMESTAMP, $HOSTNAME, $i, $NVIDIA, $USER, $APP, $MYPID 
#		pass
#	MYPID=$p
#	  fi 
#	  echo $TIMESTAMP, $HOSTNAME, $i, $NVIDIA, $USER, $APP, $UPID
done
#   else
#	echo   null, null, null
#  fi
#  echo  $TIMESTAMP, $HOSTNAME, $i, $NVIDIA, $USER, $APP, $UPID 
#  if [ "${PIDS}" != "" ] ; then


