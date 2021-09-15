import csv  
import subprocess as sp
import time 
from datetime import datetime

print("i-comit.github.io \n")
name = input("Enter the website url: ")
interval = float(input("Enter interval time in seconds: "))

now = datetime.now()
titletime= datetime.date(now).strftime("%Y%m%d")

starttime=time.time() 

with open(f'{name}-PingTest{titletime}.csv', 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(["Time", "Packet Sent", "Packet Received", "Packet Loss", "Status"])

while(True): 
    output = sp.getoutput(f'ping -n 3 {name} | find "Packets"')
    print (output)
    packetsent = output[20:21]
    packetreceived = output[34:35]


    with open(f'{name}-PingTest{titletime}.csv', 'a') as f:
        writef = csv.writer(f)
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        writef.writerow( [current_time] + [packetsent] + [packetreceived])

        time.sleep(interval - ((time.time() - starttime) % interval))
