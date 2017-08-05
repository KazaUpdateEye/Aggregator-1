#!/bin/bash
AggregatorId=$1
CameraId=$2
parent=/home/Videos/$AggregatorId/$CameraId
newfolder=/home/UploadedVideos
sleep 2;
while true
do
if [ ! -d $newfolder ]; then
echo "not exist"
mkdir "$newfolder"
fi
for folder in "$parent"/*; do
if [ -d $folder ]; then
foldername="${folder##*/}"
for file in "$parent"/"$foldername"/*; do
filename="${file##*/}"
filename1="${filename%.*}"
newfilename="$AggregatorId"_"$CameraId"_"$filename1"
echo $filename1
	echo "Calling Python"
	python /home/project/compareTimeForVod.py $parent"/"$foldername"/"$filename1.avi $CameraId &&
	value=`cat /home/Videos/$CameraId`
	echo "value"
	echo $value
	if [ $value = "Yes" ]
	then
		echo "Yes"
		#sleep 2;
		mv $parent"/"$foldername"/"$filename1.avi $parent"/"$foldername"/"$newfilename.avi &&
		python /home/project/uploadVideoToCloud.py $AggregatorId $CameraId $newfilename.avi $foldername &&
		mv $parent"/"$foldername"/"$newfilename.avi $newfolder"/"$newfilename.avi
	fi

#sleep 1;
done
fi
done
done
