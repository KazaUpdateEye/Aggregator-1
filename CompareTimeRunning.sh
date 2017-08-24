#!/bin/bash
sleep 10
while true;
do
if ps ax | grep -v grep | grep "python /home/project/compareTime.py" > /dev/null
then
echo "running"
else
python /home/project/compareTime.py &
fi
sleep 5;
done;
