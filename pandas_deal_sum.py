# -*- coding: utf-8 -*-
"""
    @Time:2018/8/29 15:55
    @Author: John Ma
"""

import pandas as pd
import re

f = open('file.txt','r')
w = open('engineering_construction_stockNumber.txt','w')

data = f.read().split('\t')
stock = []

for i in data:
    stock.extend(re.findall(r"\d{6,10}",i))
stock.sort()
for i in range(len(stock)):
    w.write(stock[i])
    if i != len(stock)-1 :
        w.write('\n')
print(len(stock))

