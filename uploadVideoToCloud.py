import os
import json
import time
import shutil
from azure.storage.blob import BlobService
import requests
import subprocess
import sys
AggregatorId= sys.argv[1]
CameraId= sys.argv[2]
fileName= sys.argv[3]
storage=sys.argv[4]
print AggregatorId
print CameraId
print fileName
print storage
directory="/home/Videos/"+AggregatorId+"/"+CameraId+"/"+storage
print directory
blobService = BlobService(account_name='changovideoanalytics', account_key='tI80QuwOnv282ttR9HmXLqJR0WosC6vC1rH5H2sBdbxsVjkARCHFGjpEmbnM5+AUbKGmy7t03VgP+JCyUl64CQ==')
#directory="/home/UploadedVideos/"
containerName="avi"

path=os.path.join(directory, fileName)
print(path)
AggregatorId,CameraId,file=fileName.split("_")
print AggregatorId
print CameraId
print file
try:
	blobService.put_block_blob_from_path(containerName,fileName,path)
	url = blobService.make_blob_url(container_name=containerName,blob_name=fileName)
	url = '{0}://{1}{2}/{3}/{4}'.format("https","changovideoanalytics",".blob.core.windows.net",containerName,fileName)
	print (url)
	time.sleep(5)
	#os.remove(path)	
except Exception as e: 
	print(e)
	pass
	


