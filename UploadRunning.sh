#!/bin/bash
while true;
do
if ps ax | grep -v grep | grep "python /home/project/UploadMotionData.py" > /dev/null
then
echo "running"
else
python /home/project/UploadMotionData.py &
fi
sleep 10;
done;
