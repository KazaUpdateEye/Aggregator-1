import os
import time
import datetime
ts = time.time()
path="/home/Videos/5c089768-958a-4a46-abda-9265ed91a35d/304d095f-7539-416a-9d86-f6a02dd4ba8c/Hybrid/fffe00d8-bf10-40e6-8cf6-659b1b47fd90.avi"
t=os.path.getmtime(path)
w=os.stat(path)
print t
print w
print ts
a=ts-t
print "diff"
print a
print(
    datetime.datetime.fromtimestamp(
        int(t)
    ).strftime('%Y-%m-%d %H:%M:%S')
)
