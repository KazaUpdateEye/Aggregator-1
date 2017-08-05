import sys
from os import path
from datetime import datetime, timedelta
two_days_ago = datetime.now() - timedelta(seconds=10)
file=sys.argv[1]
camera=sys.argv[2]
print file
filetime = datetime.fromtimestamp(path.getctime(file))
print filetime
if filetime < two_days_ago:
	with open("/home/Videos/"+camera, mode='w') as file:
    		file.write('Yes')
else:
	with open("/home/Videos/"+camera, mode='w') as file:
		file.write('No')
