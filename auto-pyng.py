import csv  
import subprocess as sp
import time 
from datetime import datetime

import sys
from PyQt5.QtWidgets import QLabel, QMainWindow,QDesktopWidget, QApplication, QTextEdit, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QTextBlock
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'AUTO PYNG 0.0.1'
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 300
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('logo.png'))
        self.center()
    
        # Create url textbox
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
        
        # Create a button in the window
        self.button = QPushButton('ENTER', self)
        self.button.move(20,80)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.button.show()

    def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    
    # @pyqtSlot()
    def on_click(self):
        name = str(self.urltext.text())
        interval = int(self.timetext.text())

        now = datetime.now()
        titletime= datetime.date(now).strftime("%Y%m%d")

        starttime=time.time() 

        with open(f'{name}-PingTest{titletime}.csv', 'w', newline="") as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Time", "Packet Sent", "Packet Received", "Packet Loss", "Status"])
        while(True):       
            output = sp.getoutput(f'ping -n 3 {name} | find "Packets"')
            print (output)
            packetsent = output[20:21]
            packetreceived = output[34:35]
            packetloss = output[44:45]

            if(packetsent == packetreceived):
                status= "UP"
            elif(packetsent <= (packetsent - 1) > 0):
                status="ERROR"
            else:
                status="DOWN"

            with open(f'{name}-PingTest{titletime}.csv', 'a', newline="") as f:
                writef = csv.writer(f)
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)

                writef.writerow([current_time] + [packetsent] + [packetreceived] + [packetloss] + [status])

                time.sleep(interval - ((time.time() - starttime) % interval))


                # QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
                # self.textbox.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

# print("i-comit.github.io \n")
# name = input("Enter the website url: ")
# interval = float(input("Enter interval time in seconds: "))

