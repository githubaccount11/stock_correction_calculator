# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 13:24:19 2020

@author: User
"""

import glob
import csv

csv_file_path = 'C:/Users/User/Documents/EODData/DataClient/ASCII/NASDAQ/1'


bull = True
bought = False
index = 0
totalProfit = 0
bears = 0
bulls = 0
zeros = 0
lastClose = 0
profitlist = []
bearstoBullslist = []
bearstoZeroslist = []
largestBearList = []
reactionList = []
timesList = []
pctChange = 0
mod = 0
daysIndex = 0
symbol = ""
time = ""
new = False
old = False
buy = False
timeIndex = 0
#34 55
for file in glob.glob(csv_file_path + '/*.csv'):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if symbol != row[0]:
                lastClose = float(row[5])
                symbol = row[0]
            if symbol == symbol:
                pctChange = (float(row[5]) - lastClose) / lastClose
                #print('pctChange: ' + str(pctChange))
                if old == True:
                    if reactionList[timeIndex] > 0:
                        bulls -= 1
                    if reactionList[timeIndex] == 0:
                        zeros -= 1
                    if pctChange > 0:
                        #print('bull added')
                        bulls += 1
                    if pctChange == 0:
                        #print('zero added')
                        zeros += 1
                    reactionList[timeIndex] = pctChange
                    #print('reactionList replaced ' + str(timeIndex) + ' with ' + str(pctChange))
                    old = False
                if new == True:
                    if pctChange > 0:
                        bulls += 1
                    if pctChange == 0:
                        zeros += 1
                    reactionList.append(pctChange)
                    #print(len(reactionList))
                    #print('reactionList stored: ' + str(pctChange) + ' at ' + str(len(timesList)))
                    bears += 1
                    buy == True
                    #print('bear added')
                    new = False
                if pctChange < 0:
                    time = row[1][(len(row[1]) - 5):]
                    #print('time: ' + str(time))
                    if time not in timesList:
                        timesList.append(time)
                        largestBearList.append(pctChange)
                        #print(len(timesList))
                        new = True
                    else:
                        timeIndex = timesList.index(time)
                        #print('timeIndex: ' + str(timeIndex))
                        if largestBearList[timeIndex] > pctChange:
                            #print('largestBearList replaced ' + str(largestBearList[timeIndex]) + ' with ' + str(pctChange))
                            largestBearList[timeIndex] = pctChange
                            old = True
                lastClose = float(row[5])
                index += 1
        for reaction in reactionList:
            totalProfit += reaction
        #print(totalProfit)
        if buy == True:
            profitlist.append(str((totalProfit) / index))
            print ('total profit per minute: ' + str(profitlist[daysIndex]))
            print ('')
            daysIndex += 1
        reactionList.clear()
        largestBearList.clear()
        timesList.clear()
        index = 0
        totalProfit = 0
        #print(totalProfit)
        new = False
        old = False
        buy = False
       
avgProfit = 0
avgBeartoBullsRatio = 0
avgBeartoZerosRatio = 0
fee = 0.000119
for x in range(0, daysIndex - 1):
    avgProfit += float(profitlist[x])
avgProfit = avgProfit / daysIndex
avgBeartoBullsRatio = bulls / bears
avgBeartoZerosRatio = zeros / bears
print('total bears: ' + str(bears))
print('fees for 1 share per bear: ' + str(bears * fee))
print('Bear to Bull ratio: ' + str(avgBeartoBullsRatio))
print('Bear to Zero ratio: ' + str(avgBeartoZerosRatio))
print ('average profit to length ratio (profit per minute): ' + str(avgProfit))
print ('or ' + str(avgProfit * 252 * (6 * 60 + 30)) + ' a year.')

"""
Bear to Bull ratio: 0.6065385064979365
Bear to Zero ratio: 0.2510643413872051
average profit to length ratio (profit per minute): 0.0004151803774586331
or 40.803927496634465 a year.
"""