from azure.storage.blob import BlobService 
blobService = BlobService(account_name='chango', account_key='h/RbA/QMVr9lyndGvaPIw3A1uugvui+RJHM5e4lOrly6/fBM2N79RW/Svbz3Rdx+rulIyWJB80f1BvmlZjXOfg==')
blobService.put_block_blob_from_path("analyticimage", "aaa", "/home/Images/7ce76956-b9bd-4f5d-b23b-6a33ce174dd4/1494b7be-4233-4096-bf8d-8470f7783633/Picture1.png")