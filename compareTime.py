import datetime
import subprocess
a = datetime.datetime.now()
file = open("/home/Aggregator/PlayLive.txt", "r") 
b = file.read()
d = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M:%S.%f") 
c = a - d
datetime.timedelta(0, 4, 316543)
TimeDifference = c.seconds/60
print TimeDifference
if TimeDifference > 10:
	rc1 = subprocess.call("/home/Aggregator/nginxUpdateToStop.sh " , shell=True)


