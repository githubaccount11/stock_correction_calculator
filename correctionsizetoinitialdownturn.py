# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 17:37:38 2020

@author: User
"""

import glob
import csv
import math

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
rounds = []
pctChange = 0
lastPctChange = 0
lastLastPctChange = 0
mod = 0
symbol = ""
posCorrections = 0
bulls = 0
bears = 0
zeros = 0
#34 55 


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

#a = True
for file in glob.glob(csv_file_path + '/*.csv'):
    #if  a:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if symbol != row[0]:
                    index = 0
                    lastClose = float(row[5])
                    symbol = row[0]
                lastLastPctChange = lastPctChange
                lastPctChange = -pctChange
                pctChange = (float(row[5]) - lastClose) / lastClose
                if bull == False and lastLastPctChange > 0:
                    bears += 1
                    if pctChange > 0:
                        bulls += 1
                        x.append(round_half_up(lastLastPctChange, 5))
                        print(round_half_up(lastLastPctChange, 5))
                        print(lastPctChange)
                        y.append(pctChange)
                        print ('correction')
                    elif pctChange == 0:
                        zeros += 1
                if pctChange > 0:
                    bull = True
                elif pctChange < 0:
                    bull = False
                print ('row: ' + str(pctChange))
                print ('index: ' + str(index))
                print ('')
                lastClose = float(row[5])
                index += 1
        #a = False
        
def power_law(x, a, b):
    return a*np.power(x, b)




index = 1
theta = []
rhos = []
thetas = []
while len(x) > 0:
    
    while index < len(x):
        """
        print('x:')
        print(x[index])
        print('y:')
        print(y[index])
        """
        if x[0] == x[index]:
            theta.append(y[index])
            #make sure rho has 3 or more points
            y.pop(index)
            x.pop(index)
        else:
            index += 1
            
    theta.append(y[0])
    rhos.append(x[0])
    thetas.append(sum(theta) / len(theta))
    x.pop(0)
    y.pop(0)
    index = 1
    
    
rhos = np.array(rhos, dtype=float)
theta = np.array(thetas, dtype=float) #so the curve_fit can work

#print(rhos)
#print('thetas: ')
#print(thetas)
popt, pcov = curve_fit(power_law, rhos, thetas, maxfev = 20000)
print("a = " + str(popt[0]) + "  b = " + str(popt[1]))

x_eval = np.linspace(min(rhos), max(rhos), 100)
        
deviation = 0
rhoIndex = 0
for val in rhos:
    deviation += abs(thetas[rhoIndex] - power_law(rhos[rhoIndex], *popt))
    rhoIndex += 1
deviation = deviation / rhoIndex
print("power law deviation: " + str(deviation))

plt.plot(rhos, theta, 'ro',label="Original Data")
plt.plot(x_eval, power_law(x_eval, *popt), label= str(rounds[0]) + ": a = " + str(popt[0]) + "  b = " + str(popt[1]))
plt.legend(loc='upper left')
plt.show()
            
            
print('finished')
#crashed at rocord number 4455

"""

a = 0.006969023188681104  b = 0.11618891768057273

power law deviation: 0.0004470233328498594
"""