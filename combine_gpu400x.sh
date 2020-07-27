#!/bin/bash
# Used to combine files for multiple dates into a single file per GPU node
for j in `seq 1 3`
do
	rm logs/gpu/gpu400$j/all 
done 


for i in `cat dates`
do 
	for j in `seq 1 3`
	do
		cat logs/gpu/gpu400$j/$i >> logs/gpu/gpu400$j/all 
	done 
done
