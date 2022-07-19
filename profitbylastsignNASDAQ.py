# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:22:23 2020

@author: User
"""

import glob
import os
import csv

csv_file_path = 'C:/Users/User/Desktop/stocks data/stocks/'


bull = True
bought = False
index = 0
falseIndex = 0
totalProfit = 0
bears = 0
bulls = 0
zeros = 0
lastClose = 0
profitlist = [0, 0, 0]
bearstoBullslist = [0, 0, 0]
bearstoZeroslist = [0, 0, 0]
pctChange = 0
mod = 0
symbolsIndex = 0
filecounter = 0

for file in glob.glob(csv_file_path + "NASDAQ" + '/*.csv'):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
            if index == 0:
                lastClose = float(row[4])
            mod = falseIndex % 2
            if mod == 0:
                pctChange = (float(row[4]) - lastClose) / lastClose
                if bull == False:
                    totalProfit = totalProfit + pctChange
                    bears += 1
                else:
                    bought = False
                if bought == False and bull == False:
                    bulls += 1
                    bought = True
                if pctChange > 0:
                    bull = True
                elif pctChange < 0:
                    bull = False
                if pctChange == 0:
                    zeros += 1
                print ('row: ' + str(pctChange))
                print ('index: ' + str(index))
                print ('total profit: ' + str(totalProfit))
                print ('')
                lastClose = float(row[4])
                index += 1
            falseIndex += 1
        if bears > 0:
            fileCounter += 1
            bearstoBullslist.append(str(bulls / bears))
            bearstoZeroslist.append(str(zeros / bears))
            profitlist.append(str((totalProfit) / index))
            symbolsIndex += 1
        index = 0
        totalProfit = 0
        bears = 0
        bulls = 0
        zeros = 0
        
avgProfit = 0
avgBeartoBullsRatio = 0
avgBeartoZerosRatio = 0
for x in range(3, symbolsIndex + 2):
    avgProfit += float(profitlist[x])
    avgBeartoBullsRatio += float(bearstoBullslist[x])
    avgBeartoZerosRatio += float(bearstoZeroslist[x])
avgProfit = avgProfit / symbolsIndex
avgBeartoBullsRatio = avgBeartoBullsRatio / symbolsIndex
avgBeartoZerosRatio = avgBeartoZerosRatio / symbolsIndex
print('Bear to Bull ratio: ' + str(avgBeartoBullsRatio))
print('Bear to Zero ratio: ' + str(avgBeartoZerosRatio))
print ('average profit to length ratio: ' + str(avgProfit))

#Bear to Bull ratio: 0.4584049309033227
#Bear to Zero ratio: 0.24871013336856151
#average profit to length ratio: 0.0011497760905928977
#avg profit a year: .2897435748293856%