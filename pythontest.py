import os
import json
import shutil
from azure.storage.blob import BlobService
import requests
blobService = BlobService(account_name='changovideoanalytics', account_key='tI80QuwOnv282ttR9HmXLqJR0WosC6vC1rH5H2sBdbxsVjkARCHFGjpEmbnM5+AUbKGmy7t03VgP+JCyUl64CQ==')
relevant_path = "/home/project/DumpJson/"
included_extenstions = ['.json']
destination_folder = 'DumpJson2/'

def PutImageToBlob(localImagePath):
    try:
        head, tail = os.path.split(localImagePath)
        blobService.put_block_blob_from_path("analyticimage", tail, localImagePath)
    except :
        pass
    


def SaveToDatabase(JsonData):
    try:
        PutImageToBlob(JsonData["LocalImage"])
        url = 'http://0f8202c8526b4c35aae76a654dd1e0a1.cloudapp.net/api/CameraVideoOnDemand/AddVideoOnDemand'
        data = {"AgreegatorId": JsonData["AgreegatorId"], "CameraId": JsonData["CameraId"], "end_date":JsonData["end_date"],"start_date":JsonData["start_date"],"text":JsonData["text"],"media":JsonData["media"]}
        response = requests.post(url, data=data)
        response.status_code
        response.text
    except :
        pass
    

while True:
    file_names = [fn for fn in os.listdir(relevant_path) if any(fn.endswith(ext) for ext in included_extenstions)]
    if len(file_names) == 0:
        print 'No File'
        continue
    for file in file_names:
        subject_path = os.path.join(relevant_path, file)
        delete_path = os.path.join(destination_folder, file)
        with open(subject_path) as data_file:
            data_loaded = json.load(data_file)
            SaveToDatabase(data_loaded)
            data_file.close()
            #shutil.move(subject_path, delete_path)
            os.remove(subject_path)
