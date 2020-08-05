#!/bin/bash
# Used to combine files for multiple dates into a single file per GPU node
# And get the research programme name per user

# Make sure folders are clean of files from previous runs
for j in `seq 1 6`
do
	rm logs/gpu/gpu200$j/all 
done 

# Generate file per GPU node
for i in `cat dates`
do 
	for j in `seq 1 6`
	do
		cat logs/gpu/gpu200$j/$i >> logs/gpu/gpu200$j/all 
	done 
done

# Replace the all file per GPU node with an equivalent file that has the research programmes per user included
#for i in '1' #`seq 1 6`
#do
#	user=[]
#	user=(`awk -F',' '{print $8}' logs/gpu/gpu200$i/all`)
#	for((j=0;j<${#user[@]};j++))
#	do
#		hits=`grep ${user[$j]} users.csv`
#		if [[ -n $hits ]]
#		then
#			prog=`echo $hits | awk -F',' '{print $2}'`
#			printf '%s %s\n' ','$prog
#		else
#			echo ",null"
#		fi 
#	done > new
#	paste logs/gpu/gpu200$i/all new > check
#	mv check logs/gpu/gpu200$i/all
#done
#rm new
