from tkinter import *
import subprocess as sp
import csv
import time 
import threading
from datetime import datetime
window=Tk()
window.geometry("600x250")
window.iconbitmap('favicon.ico')
window.title('     auto-pyng 0.1.1')
window.eval('tk::PlaceWindow . center')

window.minsize(500, 250)
window.maxsize(800, 250)

def getUrl():
    urls=[]
    name = str(e1.get().strip())
    interval = int(e2.get().strip())
    csvthread= threading.Thread(target=logCSV, args=(1,))
    now = datetime.now()
    titletime= datetime.date(now).strftime("%Y%m%d") 
    with open(f'{name}-PingTest{titletime}.csv', 'w', newline="") as outcsv:
                writer = csv.writer(outcsv)
                writer.writerow(["Time", "Packet Sent", "Packet Received", "Packet Loss", "Status"])
    csvthread.daemon = True
    csvthread.start()
    urls.append(name)
    # listvar.set(urls)
    for url in urls:
        Lb1.insert(0, url)
    
def logCSV(name):
    name = str(e1.get().strip())
    interval = int(e2.get().strip())
    namecache = name
    intervalcache = interval
    now = datetime.now()
    titletime= datetime.date(now).strftime("%Y%m%d")
    
    starttime=time.time() 
    e1.delete(0, "end")
    e2.delete(0, "end")
    while(True):       
        output = sp.getoutput(f'ping -n 3 {namecache} | find "Packets"')
        print (output)
        packetsent = output[20:21]
        packetreceived = output[34:35]
        packetloss = output[44:45]

        if(packetsent == packetreceived):
            status= "UP"
        elif(packetsent < packetreceived > 0):
            status="ERROR"
        else:
            status="DOWN"

        with open(f'{namecache}-PingTest{titletime}.csv', 'a', newline="") as f:
            writef = csv.writer(f)
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)

            writef.writerow([current_time] + [packetsent] + [packetreceived] + [packetloss] + [status])

            time.sleep(intervalcache - ((time.time() - starttime) % intervalcache))

def stopLog():
    my_string_var.set("current active logs: " + str(threading.active_count()))
    
my_string_var = StringVar()
listvar = StringVar()

lbl1 = Label(window, textvariable = my_string_var)
lbl1.place(x=250, y=50)
lb2 = Label(window, textvariable = listvar)

lbl5=Label(window, text="multithreaded automated ping logger", fg='red', font=("Helvetica", 14))
lbl5.pack(side="top", ipady=30)
l1= Label(window, text="enter website URL here \n\n\nenter time interval here",  fg='black', font=("Verdana", 8))
l1.pack(ipadx=0, padx=10, ipady=4, pady=3, side=LEFT, anchor=NE)

e1=Entry(window, bd=5)
e1.pack(ipadx=30, padx=20, ipady=4, pady=3, side=TOP, anchor=NW)

e2=Entry(window, text="enter Time here", bd=5)
e2.pack(ipadx=30, padx=20, ipady=4, pady=3, side=TOP, anchor=NW)

Lb1 = Listbox(window)
Lb1.place(relx=0.7, rely=.36, relheight=0.3, relwidth=0.25)

Start = Button(window,bg='#3F3F3F', fg='#37D028', pady=0, borderwidth=3, relief="ridge", command=lambda:[getUrl()])
Start.pack(ipadx=30, padx=20, ipady=4, pady=3, side=LEFT, anchor=NW)

Stop = Button(window,bg='red', fg='blue', pady=0, borderwidth=3, relief="ridge", command=lambda:[stopLog()])
Stop.pack(ipadx=30, padx=25, ipady=4, pady=3, side=LEFT, anchor=NW)


window.mainloop()