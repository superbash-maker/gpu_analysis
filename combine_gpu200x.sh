#!/bin/bash
# Used to combine files for multiple dates into a single file per GPU node

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
		# Check if data has been obtained for all dates in range
		if [ -f "logs/gpu/gpu200"$j"/"$i ]
		then
			cat logs/gpu/gpu200$j/$i >> logs/gpu/gpu200$j/all 
		else
			# If no data present generate with null information
			for hour in {00..23}
			do
				for min in {00..55..5}
				do
					echo $i" "$hour":"$min", gpu200"$j", 0, 00000000:3B:00.0,32,0,0, null, null, null" >> logs/gpu/gpu200$j/all
					echo $i" "$hour":"$min", gpu200"$j", 1, 00000000:AF:00.0,31,0,0, null, null, null" >> logs/gpu/gpu200$j/all
					echo $i" "$hour":"$min", gpu200"$j", 2, 00000000:D8:00.0,29,0,0, null, null, null" >> logs/gpu/gpu200$j/all
				done
			done
		fi
	done 
done
