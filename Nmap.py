import nmap
import time
import subprocess
import os
import logging

camdetailfile = '/home/project/cameradetails.txt'
logfile = '/home/project/example.log'

logging.basicConfig(filename=logfile,level=logging.DEBUG)
logging.info('Binding Servicebus')
def deleteContent(fName):
    with open(fName, "w"):
        pass

deleteContent(camdetailfile)
deleteContent(logfile)

nm = nmap.PortScanner()
nm.scan(hosts='192.168.0.0/24', arguments='-sP')
pt = nmap.PortScanner() 



f = open(camdetailfile, 'w')
saperator = '-' 
for h in nm.all_hosts(): 
    if 'mac' in nm[h]['addresses']:
        mac = nm[h]['addresses']['mac']
        ipv4 = nm[h]['addresses']['ipv4']
        pt.scan(hosts=ipv4,ports='554')
        logging.info('{0}:{1}'.format(mac, ipv4)) 
        for h in pt.all_hosts():
            state = pt[h]['tcp'][554]['state']
            name = pt[h]['tcp'][554]['name']
            pic = ''
            if state == 'open' and name == 'rtsp': 
                logging.info('{0}:{1}'.format(state, name)) 
                try:
                    subprocess.call("/home/Aggregator/camPic.sh " + ipv4, shell=True)
                    pic = ipv4 + '.jpeg'
                except ValueError:
                    pic = 'no.jpeg'
               
                f.write(mac + saperator + ipv4 + saperator + pic + '\n')
f.close()
