# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:37:58 2020

@author: User
"""

import glob
import csv

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


csv_file_path = 'C:/Users/User/Documents/EODData/DataClient/ASCII/TICK/V-Ticks-Sample'


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
bulls = 0
zeros = 0
bears = 0
totalProfit = 0
#34 55 
#2010-01-04 09:30:22:780
hours = 0
minutes = 0
finished = False
for file in glob.glob(csv_file_path + '/*.txt'):
    if file.endswith('readme') == False:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if finished == False:
                    print(row)
                    if row[0][11:13] == "00":
                        hours = 0
                    else:
                        hours = int(row[0][11:13].lstrip('0'))
                    if row[0][14:16] == "00":
                        minutes = 0
                    else:
                        minutes = int(row[0][14:16].lstrip('0'))
                    if hours >= 9:
                        if hours < 16:
                            if hours == 9:
                                if minutes >= 30:
                                    if symbol != file[0:file.find('_')]:
                                        index = 0
                                        lastClose = float(row[1])
                                        symbol = file[0:file.find('_')]
                                    lastPctChange = -pctChange
                                    pctChange = (float(row[1]) - lastClose) / lastClose
                                    if bull == False and lastPctChange > 0:
                                        bears += 1
                                        if pctChange > 0:
                                            bulls += 1
                                            x.append(lastPctChange)
                                            y.append(pctChange)
                                            totalProfit += pctChange
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
                                    lastClose = float(row[1])
                                    index += 1
                            elif int(row[0][11:13].lstrip('0')) < 16:
                                if symbol != file[0:file.find('_')]:
                                    index = 0
                                    lastClose = float(row[1])
                                    symbol = file[0:file.find('_')]
                                lastPctChange = -pctChange
                                pctChange = (float(row[1]) - lastClose) / lastClose
                                if bull == False and lastPctChange > 0:
                                    bears += 1
                                    if pctChange > 0:
                                        bulls += 1
                                        x.append(lastPctChange)
                                        y.append(pctChange)
                                        totalProfit += pctChange
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
                                lastClose = float(row[1])
                                index += 1
                        else:
                            finished = True
        bull = True
             
        
plt.plot(x, y, 'ro',label="Original Data")

x = np.array(x, dtype=float) #transform your data in a numpy array of floats 
y = np.array(y, dtype=float) #so the curve_fit can work

def power_law(x, a, b):
    return a*np.power(x, b)

popt, pcov = curve_fit(power_law, x, y)

print("a = " + str(popt[0]) + "  b = " + str(popt[1]))

x_eval = np.linspace(min(x), max(x), 100)

xIndex = 0
deviation = 0
for val in x:
    deviation += abs(y[xIndex] - power_law(x[xIndex], *popt))
    xIndex += 1
deviation = deviation / xIndex

print("power law deviation: " + str(deviation))
plt.legend(loc='upper left')
plt.show()

plt.plot(x, y, 'ro',label="Original Data")
plt.plot(x_eval, power_law(x_eval, *popt), label="Power Law Fitted Curve")
plt.legend(loc='upper left')
plt.show()

avgProfit = 0
avgBeartoBullsRatio = 0
avgBeartoZerosRatio = 0
fee = 0.000119
avgProfit = totalProfit / index
avgBeartoBullsRatio = bulls / bears
avgBeartoZerosRatio = zeros / bears
print('total bears: ' + str(bears))
print('fees for 1 share per bear: ' + str(bears * fee))
print('Bear to Bull ratio: ' + str(avgBeartoBullsRatio))
print('Bear to Zero ratio: ' + str(avgBeartoZerosRatio))
print ('average profit to length ratio (profit per tick): ' + str(avgProfit))
print ('or ' + str(totalProfit * 252) + ' a year.')

"""
APPL:
a = 0.6276586325357923  b = 0.9600922697920323
power law deviation: 4.0654109167420235e-05
total bears: 22249
fees for 1 share per bear: 2.647631
Bear to Bull ratio: 0.42572699896624566
Bear to Zero ratio: 0.3843768259247607
average profit to length ratio (profit per tick): 8.907319646934113e-06
or 202.32777054050746 a year.
"""
"""
GOOG:
a = 0.03206122091605021  b = 0.6020054366086186
power law deviation: 8.587789371528178e-05
total bears: 4004
fees for 1 share per bear: 0.476476
Bear to Bull ratio: 0.4383116883116883
Bear to Zero ratio: 0.233016983016983
average profit to length ratio (profit per tick): 2.034383308005599e-05
or 57.94135237063979 a year.
"""

"""
TSLA:
a = 1.3552568437808636  b = 1.092805075800478
power law deviation: 0.000570343672976213
total bears: 14141
fees for 1 share per bear: 1.682779
Bear to Bull ratio: 0.3785446573792518
Bear to Zero ratio: 0.4518068029135139
average profit to length ratio (profit per tick): 7.372674485216192e-05
or 1367.610473519045 a year.
"""

"""
T:
a = 0.43338290690326237  b = 0.9083225606021719
power law deviation: 7.955892108966094e-05
total bears: 9520
fees for 1 share per bear: 1.13288
Bear to Bull ratio: 0.4566176470588235
Bear to Zero ratio: 0.3769957983193277
average profit to length ratio (profit per tick): 1.0705958162373936e-05
or 234.29925202606387 a year.
"""

"""
AMZN:
a = 0.044386663492063314  b = 0.6292005399670896
power law deviation: 9.247671265015833e-05
total bears: 10094
fees for 1 share per bear: 1.201186
Bear to Bull ratio: 0.40043590251634636
Bear to Zero ratio: 0.38547652070536953
average profit to length ratio (profit per tick): 1.7070732676828104e-05
or 169.95218583758887 a year.
"""

"""
FB:
a = 1.0395692370056473  b = 1.0241169070659732
power law deviation: 0.0004955760682565096
total bears: 214110
fees for 1 share per bear: 25.479090000000003
Bear to Bull ratio: 0.4036523282424922
Bear to Zero ratio: 0.4460557657278969
average profit to length ratio (profit per tick): 0.00010369335052216389
or 31068.595047076313 a year.
"""

"""
JNJ:
a = 0.8795408469729401  b = 0.9972822597362248
power law deviation: 4.397697516063975e-05
total bears: 5202
fees for 1 share per bear: 0.619038
Bear to Bull ratio: 0.41810841983852365
Bear to Zero ratio: 0.4542483660130719
average profit to length ratio (profit per tick): 6.476407711100584e-06
or 65.59717629333097 a year.
"""

"""
MSFT:
a = 1.0804249937101444  b = 1.0260603645114474
power law deviation: 9.407432565782777e-05
total bears: 10250
fees for 1 share per bear: 1.2197500000000001
Bear to Bull ratio: 0.4589268292682927
Bear to Zero ratio: 0.3791219512195122
average profit to length ratio (profit per tick): 1.098613990579092e-05
or 254.15450313911734 a year.
"""

"""
NFLX:
a = 0.7433386112253034  b = 0.9704530952794419
power law deviation: 0.0001775220886336369
total bears: 3089
fees for 1 share per bear: 0.367591
Bear to Bull ratio: 0.37034639041761086
Bear to Zero ratio: 0.4308837811589511
average profit to length ratio (profit per tick): 3.0404339552995766e-05
or 104.44693311018244 a year.
"""

"""
V:
a = 0.05080341628094161  b = 0.6518272520460462
power law deviation: 6.706840173001484e-05
total bears: 5315
fees for 1 share per bear: 0.6324850000000001
Bear to Bull ratio: 0.39943555973659456
Bear to Zero ratio: 0.45117591721542805
average profit to length ratio (profit per tick): 1.2016884229338786e-05
or 82.05359275969727 a year.
"""

print((82.05359275969727 + 104.44693311018244 + 254.15450313911734 + 65.59717629333097 + 31068.595047076313 + 169.95218583758887 + 234.29925202606387 + 1367.610473519045 + 57.94135237063979 + 202.32777054050746) / 10)
"""
or 3360.697828667248 a year on avg
"""