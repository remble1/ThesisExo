import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from MainWindow import Ui_MainWindow
from time import sleep
import time
import Adafruit_ADS1x15
from map_func import *
from datetime import datetime, date

filename = 'axis.txt'
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()

GAIN = 1
adc = Adafruit_ADS1x15.ADS1115()
with open(filename, 'a') as file_object:
    file_object.write(f"Zaczynamy zapis danych, {current_time}, {today} \n")


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):  # argumenty konstruktora
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self) # oddziedziczyłem to

class Worker(QThread):
    def run(self):
        while True:
            values = [0]*3
            for i in range(3):
                values[i] = adc.read_adc(i, gain=GAIN)
            
            nadgarstek = nadgarstek_func(values[2])
            obrot = obrot_func(values[1])
            lokiec = lokiec_func(values[0])    
                
            window.lcdNumber_1.display("%.1f" % nadgarstek ) # formatowanie stringa
            window.lcdNumber_2.display("%.1f" % obrot )
            window.lcdNumber_3.display("%.1f" % lokiec )
            with open(filename, 'a') as file_object:
                file_object.write(f'Nadgarstek: {"%.1f" % nadgarstek }, Obrot reki: {"%.1f" % obrot }, Lokiec: {"%.1f" % lokiec }\n')   
                           
            sleep(0.1)   
            


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
thread = Worker()
thread.start()
window.show()
app.exec()