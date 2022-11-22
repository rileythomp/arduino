
import time
import pyfirmata
import matplotlib.pyplot as plt

board = pyfirmata.Arduino('COM5')
it = pyfirmata.util.Iterator(board)
it.start()

#find the steinhart coefficients to find the temp
def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
    import math
    steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
    steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
    steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
    return steinhart

#set pin 5 as digital input

board.analog[0].mode = pyfirmata.INPUT
thermistor=board.analog[0]
timeinput=100
temperature=[]
t=[0]

#read the thermistor value and append the temperature and time in order to plot later
for i in range(timeinput):
    print(board.analog[0].read())
    R = 10000 / (65535/thermistor.read() - 1)
    T=steinhart_temperature_C(R)
    temperature.append(T)
    t.append(t[i]+0.1)
    time.sleep(0.1)
    # print(board.analog[0].read())

#plot the temperature against time

plt.plot(t,temperature)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')
plt.show()