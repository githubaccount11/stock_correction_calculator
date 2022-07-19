# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 23:41:15 2020

@author: User
"""

import glob
import os
import csv

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import sympy as sym


csv_file_path = 'C:/Users/User/Documents/EODData/DataClient/ASCII/NASDAQ/1'


bull = True
index = 0
lastClose = 0
y = []
x = []
pctChange = 0
lastPctChange = 0
mod = 0
symbol = ""
posCorrections = 0
charging = 0
raging = 0
#34 55 
for file in glob.glob(csv_file_path + '/*.csv'):
    while posCorrections < 1000:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if symbol != row[0]:
                    index = 0
                    lastClose = float(row[5])
                    symbol = row[0]
                lastPctChange = -pctChange
                pctChange = (float(row[5]) - lastClose) / lastClose
                if pctChange > 0:
                    if bull == False:
                        x.append(raging)
                        raging = 0
                    charging += pctChange
                    bull = True
                elif pctChange < 0:
                    if bull == True and len(y) == len(x) - 1:
                        posCorrections += 1
                        y.append(charging)
                        print ('correction')
                        charging = 0
                    raging -= pctChange
                    bull = False
                print ('row: ' + str(pctChange))
                print ('index: ' + str(index))
                print ('')
                lastClose = float(row[5])
                index += 1
if len(x) > len(y):
    x.pop(len(x) - 1)
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
def func(x, a, b, c):
  return a * x * x + b * x + c

#def func2(x, a, b, c):
#  return a * np.log(b * x) + c


"""
make the curve_fit
"""
popt, pcov = curve_fit(func, x, y)
#popt2, pcov2 = curve_fit(func2, x, y)

"""
The result is:
popt[0] = a , popt[1] = b, popt[2] = c and popt[3] = d of the function,
so f(x) = popt[0]*x**3 + popt[1]*x**2 + popt[2]*x + popt[3].
"""
print("exponential a = " + str(popt[0]) + "  b = " + str(popt[1]) + "  c = " + str(popt[2]))
#print("logarithmic a = " + str(popt[0]) + "  b = " + str(popt[1]) + "  c. = " + str(popt[2]))

"""
Print the coefficients and plot the funcion.
"""

x_eval = np.linspace(min(x), max(x), 100)

xIndex = 0
deviation = 0
#deviation2 = 0ok   k
for val in x:
    deviation += abs(y[xIndex] - func(x, *popt))
    #deviation2 += abs(y[xIndex] - func2(x, *popt2))
    xIndex += 1
deviation = deviation / xIndex
#deviation2 = deviation2 / xIndex

print("exponential deviation: " + str(deviation))
#print("logarithmic deviation: " + str(deviation2))
plt.plot(x_eval, func(x_eval, *popt), label="Exp Fitted Curve")
#plt.plot(x, func(x, *popt), label="Fitted Curve") #same as line above \/
#plt.plot(x, popt[0]*x**3 + popt[1]*x**2 + popt[2]*x + popt[3], label="Fitted Curve") 

plt.legend(loc='upper left')
plt.show()

plt.plot(x_eval, func2(x_eval, *popt), label="Log Fitted Curve")
#plt.plot(x, func(x, *popt), label="Fitted Curve") #same as line above \/
#plt.plot(x, popt[0]*x**3 + popt[1]*x**2 + popt[2]*x + popt[3], label="Fitted Curve") 

plt.legend(loc='upper left')
plt.show()

"""
y = ax^2 + bx + c
a = 8.109550609185609  b = 0.4610831675265282  c = 0.0059320528604908124
"""