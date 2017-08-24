import sys
ip= sys.argv[1]
mac= sys.argv[2]
camid= sys.argv[3]
filename= sys.argv[4]
if filename == '/home/Aggregator/camfind.sh':
	text_file = open("/home/project/AddCamera.txt", "a")
	text_file.write("IP "+ip+" mac "+mac+" cameraId "+camid+"\n")
	text_file.close()
else:
	text_file = open("/home/project/ChangeCamera.txt", "a")
        text_file.write("IP "+ip+" mac "+mac+" cameraId "+camid+"\n")
        text_file.close()
