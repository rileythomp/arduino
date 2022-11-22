
import time
import pyfirmata
import matplotlib.pyplot as plt

board = pyfirmata.Arduino('/dev/tty.usbmodem143301')
it = pyfirmata.util.Iterator(board)
it.start()

#find the steinhart coefficients to find the temp
def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
    import math
    steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
    steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
    steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
    return steinhart

r1 = 10000
c1 = 1.009249522e-03
c2 = 2.378405444e-04
c3 = 2.019202697e-07

vcc = 5
r = 10000
rt0 = 10000
b = 3977
t0 = 22 + 273.15

#set pin 5 as digital input
board.analog[0].mode = pyfirmata.INPUT
thermistor = board.analog[0]
timeinput = 1000
temps = []
times = []

#read the thermistor value and append the temperature and time in order to plot later
time.sleep(10)
for i in range(timeinput):
    time.sleep(0.01)

    # print(thermistor.read())
    # R = 10000 / (65535/thermistor.read() - 1)
    # T=steinhart_temperature_C(R)

    # v0 = thermistor.read()
    # r2 = r1 * ((1023 / v0) - 1)
    # import math
    # logr2 = math.log(r2)
    # t = (1 / (c1 + c2*logr2 + c3*logr2*logr2*logr2))
    # tc = t - 273.15

    # vrt = thermistor.read()
    # crt = (5/1023) * vrt
    # vr = vcc - vrt
    # rt = vrt / (vr/r)
    # import math
    # ln = math.log(rt/rt0)
    # tx = (1 / ((ln / b) + (1 / t0)))
    # tc = tx - 273.15

    tc = thermistor.read()

    print(i*0.01, tc)
    temps.append(tc)
    times.append(i*0.01)

# plot the temperature against time
plt.plot(times, temps)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')
plt.show()