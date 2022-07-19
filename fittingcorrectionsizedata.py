# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 10:38:39 2020

@author: User
"""


import glob
import csv

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


csv_file_path = 'C:/Users/User/Documents/EODData/DataClient/ASCII/NASDAQ/1'


bull = True
bought = False
index = 0
lastClose = 0
y = []
x = []
reactionList = []
pctChange = 0
lastPctChange = 0
mod = 0
symbol = ""
posCorrections = 0
#34 55 
for file in glob.glob(csv_file_path + '/*.csv'):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if symbol != row[0]:
                index = 0
                lastClose = float(row[5])
                symbol = row[0]
            lastPctChange = -pctChange
            pctChange = (float(row[5]) - lastClose) / lastClose
            if bull == False and pctChange > 0:
                posCorrections += 1
                x.append(lastPctChange)
                y.append(pctChange)
                print ('correction')
            if pctChange > 0:
                bull = True
            elif pctChange < 0:
                bull = False
            print ('row: ' + str(pctChange))
            print ('index: ' + str(index))
            print ('')
            lastClose = float(row[5])
            index += 1
        
"""
x = [0.0009425070688029959,
0.0009398496240601303,
0.0018779342723004293,
0.004694835680751241,
0.0009425070688029959,
0.004734848484848552,
0.0018993352326685255,
0.0009460737937558928]
y = [0.0028301886792453904,
0.003762935089369628,
0.001881467544684814,
0.0009433962264150743,
0.0028301886792453904,
0.0019029495718363059,
0.0038058991436727804,
0.0018939393939393534]
"""

"""
Plot your data
"""
plt.plot(x, y, 'ro',label="Original Data")

"""
brutal force to avoid errors
"""

x = np.array(x, dtype=float) #transform your data in a numpy array of floats 
y = np.array(y, dtype=float) #so the curve_fit can work

"""
create a function to fit with your data. a, b, c and d are the coefficients
that curve_fit will calculate for you. 
In this part you need to guess and/or use mathematical knowledge to find
a function that resembles your data
"""
def exp(x, a, b, c):
  return a * x**2 + b * x + c

#def func2(x, a, b, c):
#  return a * np.log(b * x) + c

def power_law(x, a, b):
    return a*np.power(x, b)

"""
make the curve_fit
"""
#popt, pcov = curve_fit(exp, x, y)
popt2, pcov2 = curve_fit(power_law, x, y)

"""
The result is:
popt[0] = a , popt[1] = b, popt[2] = c and popt[3] = d of the function,
so f(x) = popt[0]*x**3 + popt[1]*x**2 + popt[2]*x + popt[3].
"""
#print("a = " + str(popt[0]) + "  b = " + str(popt[1]) + "  c = " + str(popt[2]))
print("a = " + str(popt2[0]) + "  b = " + str(popt2[1]))

"""
Print the coefficients and plot the funcion.
"""

x_eval = np.linspace(min(x), max(x), 100)

xIndex = 0
deviation = 0
deviation2 = 0
for val in x:
    #deviation += abs(y[xIndex] - exp(x[xIndex], *popt))
    deviation2 += abs(y[xIndex] - power_law(x[xIndex], *popt2))
    xIndex += 1
#deviation = deviation / xIndex
deviation2 = deviation2 / xIndex

#print("exponential deviation: " + str(deviation))
print("power law deviation: " + str(deviation2))
#plt.plot(x_eval, exp(x_eval, *popt), label="Exp Fitted Curve")
#plt.plot(x, func(x, *popt), label="Fitted Curve") #same as line above \/
#plt.plot(x, popt[0]*x**3 + popt[1]*x**2 + popt[2]*x + popt[3], label="Fitted Curve") 

plt.legend(loc='upper left')
plt.show()

plt.plot(x, y, 'ro',label="Original Data")
plt.plot(x_eval, power_law(x_eval, *popt2), label="Power Law Fitted Curve")
plt.legend(loc='upper left')
plt.show()

#plt.plot(x, func(x, *popt), label="Fitted Curve") #same as line above \/
#plt.plot(x, popt[0]*x**3 + popt[1]*x**2 + popt[2]*x + popt[3], label="Fitted Curve") 

#plt.legend(loc='upper left')
#plt.show()

"""
y = ax^2 + bx + c
a = 10.69224101105912  b = -0.9753502991485798  c = 0.004863498290448076
exp deviation: 0.00537241070822692
"""

"""
a*np.power(x, b)
a = 11.409566530516413  b = 3.1693371153962167
power law deviation: 0.003402649737657798
"""