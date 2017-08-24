import subprocess
import os
with open('/home/project/AddCamera.txt') as fp:
    for line in fp:
	myMAC = [x for x in line.split()]
 	rc = subprocess.call("sh /home/Aggregator/macaddresToIp.sh " + str(myMAC[5])+" "+ str(myMAC[3]), shell=True)
	file = open("/home/project/ChangeCamera.txt", "r")
	b = file.read()
	myIp = [a for a in b.split()]
	if myIp[1]== myMAC[1]:
		ip=myMAC[1]
	else:
		ip=myIp[1]
		rc = subprocess.call("sh /home/Aggregator/newcrontan.sh " + str(myMAC[1])+" "+str(myIp[1]), shell=True)
	compare_file = open("/home/project/cameraMatch.txt", "a")
	compare_file.write("IP "+ip+" mac "+myMAC[3]+" cameraId "+myMAC[5]+"\n")
	os.remove('/home/project/ChangeCamera.txt')
os.remove('/home/project/AddCamera.txt')
os.rename('/home/project/cameraMatch.txt','/home/project/AddCamera.txt')
