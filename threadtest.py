import logging
import random
import sys
import csv  
import time
from datetime import datetime
import subprocess as sp

from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit
)

logging.basicConfig(format="%(message)s", level=logging.INFO)

# 1. Subclass QRunnable
class Runnable(QRunnable):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.exiting = False

    def run(self):
        obj = Window()
        obj.runTasks()

        with open(f'{obj.name}-PingTest{obj.titletime}.csv', 'w', newline="") as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Time", "Packet Sent", "Packet Received", "Packet Loss", "Status"])
    
        while(self.exiting==False):
            output = sp.getoutput(f'ping -n 3 {obj.name} | find "Packets"')
            print (output)
            packetsent = int(output[20:21])
            packetreceived = int(output[34:35])
            packetloss = int(output[44:45])

            if(packetsent == packetreceived):
                status= "UP"
            elif(packetsent <= (packetsent - 1) > 0):
                status="ERROR"
            else:
                status="DOWN"

            with open(f'{obj.name}-PingTest{obj.titletime}.csv', 'a', newline="") as f:
                writef = csv.writer(f)
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)

                writef.writerow([current_time] + [packetsent] + [packetreceived] + [packetloss] + [status])

                time.sleep(obj.interval - ((time.time() - obj.starttime) % obj.interval))


                # QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
                # self.textbox.setText("")


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("QThreadPool + QRunnable")
        self.resize(550, 550)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets

        self.urltext = QLineEdit(self)
        self.urltext.move(20, 20)
        self.urltext.resize(200,20)
        self.textbox = QLabel("ENTER WEBSITE URL HERE", self)
        self.textbox.move(240, 20)
        self.textbox.resize(200,20)      

        # Create time interval textbox
        self.timetext = QLineEdit(self)
        self.timetext.move(20, 60)
        self.timetext.resize(200,20)
        self.textbox = QLabel("ENTER TIME INTERVAL HERE", self)
        self.textbox.move(240, 60)
        self.textbox.resize(200,20)   
        
        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        countBtn = QPushButton("Click me!")
        countBtn.clicked.connect(self.runTasks)
        # Set the layout
        layout = QVBoxLayout()
        # layout.addWidget(self.label)
        layout.addWidget(countBtn)
        self.centralWidget.setLayout(layout)

    def runTasks(self):
        self.name = "uberstrainer.com"
        # self.name = str(self.urltext.text())
        self.interval = 10

        now = datetime.now()
        self.titletime= datetime.date(now).strftime("%Y%m%d")
        self.starttime=time.time() 
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        # self.label.setText(f"Running {threadCount} Threads")
        pool = QThreadPool.globalInstance()
        # for i in range(threadCount):
        #     # 2. Instantiate the subclass of QRunnable
        runnable = Runnable(self)
        # 3. Call start()
        pool.start(runnable)

def main():    
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()