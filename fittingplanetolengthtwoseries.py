# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:13:35 2020

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


for file in glob.glob(csv_file_path + '/*.csv'):
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
                    rounds.append(round_half_up(lastLastPctChange, 5))
                    print(round_half_up(lastLastPctChange, 5))
                    x.append(lastPctChange)
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
        
        
def power_law(x, a, b):
    return a*np.power(x, b)


index = 1
rho = []
theta = []
rhos = []
numberofgraphs = 0
numberoffittings = 1
while 0 < len(rounds):
    rho.append(x[0])
    theta.append(y[0])
    while index < len(rounds):
        if rounds[0] == rounds[index]:
            rho.append(x[index])
            theta.append(y[index])
            #make sure rho has 3 or more points
            if len(rhos) < 3:
                if rhos.count(rho[len(rho) - 1]) == 0:
                    rhos.append(rho[len(rho) - 1])
            x.pop(index)
            y.pop(index)
            rounds.pop(index)
        else:
            index += 1
    if len(rhos) == 3:
        rho = np.array(rho, dtype=float) #transform your data in a numpy array of floats 
        theta = np.array(theta, dtype=float) #so the curve_fit can work
        
        #print(rho)
        #print(theta)
        print("First Bear: " + str(rounds[0]))
        print("record number: " + str(numberoffittings))
        popt, pcov = curve_fit(power_law, rho, theta, maxfev = 20000)
        print("a = " + str(popt[0]) + "  b = " + str(popt[1]))
        if numberofgraphs < 10:
            
            x_eval = np.linspace(min(rho), max(rho), 100)
            
            rhoIndex = 0
            deviation = 0
            for val in rho:
                deviation += abs(theta[rhoIndex] - power_law(rho[rhoIndex], *popt))
                rhoIndex += 1
            deviation = deviation / rhoIndex
            print("power law deviation: " + str(deviation))
            
            plt.plot(rho, theta, 'ro',label="Original Data")
            plt.plot(x_eval, power_law(x_eval, *popt), label= str(rounds[0]) + ": a = " + str(popt[0]) + "  b = " + str(popt[1]))
            plt.legend(loc='upper left')
            plt.show()
            
        numberofgraphs += 1
        numberoffittings += 1
    rhos = []
    rho = []
    theta = []
    index = 1
    x.pop(0)
    y.pop(0)
    rounds.pop(0)
            
            
print('zeros: ' + str(zeros/bears))
print('bulls: ' + str(bulls/bears))
#crashed at rocord number 4455

"""
zeros: 0.20708984526085583
bulls: 0.43488394513869
"""