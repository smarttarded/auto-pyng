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

window.minsize(600, 250)
window.maxsize(600, 250)

def getUrl():
    urls=[]
    name = str(e1.get().strip())
    interval = int(dropdownoptions[dropdownlist.get()])
    print(interval)
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
    interval = int(dropdownoptions[dropdownlist.get()])
    namecache = name
    intervalcache = interval
    now = datetime.now()
    titletime= datetime.date(now).strftime("%Y%m%d")
    
    starttime=time.time() 
    e1.delete(0, "end")
    # e2.delete(0, "end")
    while(True):       
        output = sp.getoutput(f'ping -n 3 {namecache} | find "Packets"')
        # print (output)
        packetsent = output[20:21]
        packetreceived = output[34:35]
        packetloss = output[44:45]

        if(packetsent == packetreceived):
            status= "UP"
        elif(packetsent == packetloss):
            status="DOWN"
        else:
            status="ERROR"

        with open(f'{namecache}-PingTest{titletime}.csv', 'a', newline="") as f:
            writef = csv.writer(f)
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)

            writef.writerow([current_time] + [packetsent] + [packetreceived] + [packetloss] + [status])

            time.sleep(intervalcache - ((time.time() - starttime) % intervalcache))


tipiterator = 0
def stopLog():
    global tipiterator
    tipiterator += 1
    active_threads = int(threading.active_count() -1)
    if(tipiterator == 4):
        tipiterator = 0
    tiplist=[
        "Created By Khiem G Luong",
        "Current Active Logs: " + str(active_threads),
        "Do Not Have Too Many (+4) Logs",
        "Logging Will Stop On Window Close"
    ]
    
    my_string_var.set(tiplist[tipiterator])

    
my_string_var = StringVar()
listvar = StringVar()



lbl5=Label(window, text="Multithreaded Automated Ping Logger", fg='red', font=("Helvetica", 14))
lbl5.pack(side="top", ipady=30)
l1= Label(window, text="Enter Website URL Here \n\n\nEnter Time Interval Here",  fg='black', font=("Verdana", 9))
l1.pack(ipadx=0, padx=10, ipady=4, pady=3, side=LEFT, anchor=NE)
lbl1 = Label(window, text="hello world", textvariable=my_string_var, fg='black', font=("Verdana", 9))
lbl1.place(x= 150, y=190, width=300, height=30)
e1=Entry(window, bd=5)
e1.pack(ipadx=30, padx=20, ipady=4, pady=3, side=TOP, anchor=NW)

dropdownlist = StringVar(window)
dropdownoptions = {
    'Every 5 Seconds': 5,
    'Every 15 Seconds': 15, 
    'Every 30 Seconds': 30,
    'Every Minute': 60,
    'Every 5 Minutes' : 300,
    'Every 15 Minutes' : 900,
    'Every 30 Minutes' : 1800,
    'Every Hour' : 3600,
}

dropdownlist.set('Every 5 Seconds') # set the default option

dropdown = OptionMenu(window, dropdownlist, *dropdownoptions)
dropdown.pack(ipadx=30, padx=20, ipady=4, pady=3, side=TOP, anchor=NW)

# e2=Entry(window, bd=5)
# e2.pack(ipadx=30, padx=20, ipady=4, pady=3, side=TOP, anchor=NW)

Lb1 = Listbox(window)
Lb1.place(relx=0.7, rely=.36, relheight=0.3, relwidth=0.25)

Start = Button(window,bg='#3F3F3F', fg='white', text="START", pady=0, borderwidth=3, relief="ridge", command=lambda:[getUrl()])
Start.place(relx=0.05, rely=0.75, width=100, height=30)

Help = Button(window,bg='red', fg='white', text="HELP", pady=0, borderwidth=3, relief="ridge", command=lambda:[stopLog()])
Help.place(relx=0.75, rely=0.75, width=100, height=30)


window.mainloop()
