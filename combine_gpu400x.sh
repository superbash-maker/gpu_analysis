#!/bin/bash
# Used to combine files for multiple dates into a single file per GPU node

# Make sure folders are clean of files from previous runs
for j in `seq 1 3`
do
	rm logs/gpu/gpu400$j/all 
done 


# Generate file per GPU node
for i in `cat dates`
do 
	for j in `seq 1 3`
	do
		# Count the lines for each file and ensure everything is present
		count=`cat logs/gpu/gpu400$j/$i | wc -l`
		# Should we have count less then 864 remove file
		if [ $count -lt 1152 ]
		then	
			rm logs/gpu/gpu400$j/$i
		fi
		# Check if data has been obtained for all dates in range
		if [ -f "logs/gpu/gpu400"$j"/"$i ]
		then
			cat logs/gpu/gpu400$j/$i >> logs/gpu/gpu400$j/all 
		else
			# If no data present generate with null information
			for hour in {00..23}
			do
				for min in {00..55..5}
				do
					echo $i" "$hour":"$min", gpu400"$j", 0, 00000000:1A:00.0,38,36,5, null, null, null" >> logs/gpu/gpu400$j/all
					echo $i" "$hour":"$min", gpu400"$j", 1, 00000000:1C:00.0,34,0,0, null, null, null" >> logs/gpu/gpu400$j/all
					echo $i" "$hour":"$min", gpu400"$j", 2, 00000000:1D:00.0,35,0,0, null, null, null" >> logs/gpu/gpu400$j/all
					echo $i" "$hour":"$min", gpu400"$j", 3, 00000000:1E:00.0,35,0,0, null, null, null" >> logs/gpu/gpu400$j/all
				done
			done
		fi
	done 
done
