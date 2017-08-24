#!/bin/bash
parent=/home/project/DumpJson

for file in "$parent"/*; do
filename="${file##*/}"
echo $filename
filesize=$( ls -nl $parent"/"$filename | awk '{print $5}')
echo $filesize
if [ "$filesize" -lt 1 ]
then
	echo "removing "$parent"/"$filename
        rm $parent"/"$filename
fi
done
