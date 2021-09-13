
import csv  
import subprocess as sp
import time 

print("i-comit.github.io \n")
name = input("Enter the website url: ")
interval = float(input("Enter interval time in seconds: "))


starttime=time.time() 

while(True): 
    output = sp.getoutput(f'ping -n 3 {name} | find "Packets"')
    print (output)

    with open(f'{name}-ping.csv', 'a') as f:
        writef = csv.writer(f)

        # write the header
        writef.writerow([output])

        time.sleep(interval - ((time.time() - starttime) % interval))


