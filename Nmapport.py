import nmap 
nm = nmap.PortScanner() 
nm.scan(hosts='192.168.0.108',ports='554')
for h in nm.all_hosts():
    print(nm[h]['tcp'][554]['state'])
    print(nm[h]['tcp'][554]['name'])
time.sleep(5) 