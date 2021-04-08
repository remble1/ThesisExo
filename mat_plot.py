import random
from itertools import count # fajny patencik, pętla w tle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from map_func import *
import Adafruit_ADS1x15

GAIN = 1
adc = Adafruit_ADS1x15.ADS1115()

    
plt.style.use('seaborn')

x_vals = []

a_vals = []
b_vals = []
c_vals = []

index = count(step=0.1) # długość kroku


def animate(i):
    
    values = [0]*3
    for i in range(3):
        values[i] = adc.read_adc(i, gain=GAIN)
    
    nadgarstek = nadgarstek_func(values[2])
    obrot = obrot_func(values[1])
    lokiec = lokiec_func(values[0])
    
    x_vals.append(next(index))    # nalicza co 1 do góry co 0.1s

    a_vals.append(lokiec) # Lokiec 
    b_vals.append(nadgarstek) # Nadgarstek 
    c_vals.append(obrot) # Obrot reki

    

    plt.cla() # czyści ekran
    plt.plot(x_vals, a_vals, label = "Łokieć") # robi plota z list
    plt.plot(x_vals, b_vals, label = "Nadgarstek")
    plt.plot(x_vals, c_vals, label = "Obrót ręki")
    plt.subplots_adjust(top=0.85, bottom=0.09)
    plt.title("Zmiany kątów osi na żywo", {"color":"black"}, size=25, y=1.05)
    plt.ylabel("Kąt wychylenia (stopnie)")
    plt.xlabel("Czas (0.1s)")
    plt.ylim(-90, 180)
    plt.legend(bbox_to_anchor=(1, 1),
           bbox_transform=plt.gcf().transFigure)

    if len(x_vals) > 100: # mój warunek - szerokość obserwacji
        del x_vals[0], a_vals[0], b_vals[0], c_vals[0] # usuwanko


ani = FuncAnimation(plt.gcf(), animate, interval=100)


plt.plot(x_vals, a_vals, x_vals, c_vals)

plt.tight_layout()
plt.show()