import datetime

with open("PlayLive.txt", mode='w') as file:
    file.write('%s' % 
               (datetime.datetime.now()))
