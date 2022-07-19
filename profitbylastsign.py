# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 19:27:19 2020

@author: User
"""

import pandas as pd

dataset = f'BTCData/BTC2.csv'  # get the full path to the file.
df = pd.read_csv(dataset, names=['pct_change', 'volume'])  # read in specific file


totalProfit = 0
length = len(df.index)

transactions = 0
fee = .716 #USD
bull = True
bought = False
print (bull)
print (totalProfit)
index = 0
bears = 0
zeros = 0
for row in df['pct_change'][:]:
    if bull == False:
        #print(row)
        totalProfit = totalProfit + df['pct_change'][index]
        bears += 1
    else:
        bought = False
    if bought == False and bull == False:
        transactions = transactions + 1
        bought = True
    if row > 0:
        bull = True
    elif row < 0:
        bull = False
    if row == 0:
        zeros += 1
    print ('row: ' + str(df['pct_change'][index]))
    print ('index: ' + str(index))
    print ('completion: ' + str(index / length))
    print ('total profit: ' + str(totalProfit))
    print ('')
    index += 1
cost = fee * transactions
print('Bear to Bull ratio: ' + str(transactions / bears))
print('Bear to Zero ratio: ' + str(transactions / bears))
print('cost: ' + str(cost))
print ('total profit: ' + str(totalProfit))