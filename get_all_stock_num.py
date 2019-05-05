# -*- coding: utf-8 -*-
"""
    @Time:2019/4/9 9:31
    @Author: John Ma
"""
import sys
import io
import os
import lxml
import pymysql
from pyquery import PyQuery as pq
import requests
from pandas.core.frame import DataFrame
from sqlalchemy import create_engine
import pandas as pd
from download_stock_data import function_download_stock_data

def getCodes():
    codes = []
    url = 'http://quote.eastmoney.com/stock_list.html'
    req = requests.get(url, timeout=30)
    reporthtml = req.text
    html = pq(reporthtml)
    # print(html)
    stock_a_list = html("#quotesearch ul li a[target='_blank']").items()
    list_sname = []
    list_num = []
    for stock_a in stock_a_list:
        num = stock_a.text().split('(')[1].strip(')')
        if (num.startswith('1') or num.startswith('5') or num.startswith('2')): continue  # 只需要6*/0*/3*/2*开头的股票0

        sname = stock_a.text().split('(')[0]
        record = {}  # 用于存储个股的代码，和名称
        # 进行转码
        sname = sname.encode("iso-8859-1").decode('gbk').encode('utf-8')
        result = str(sname, encoding='utf-8')
        record["sname"] = result
        list_sname.append(result)
        record["num"] = num;
        list_num.append(num)
        codes.append(record)
    dict_all_stock = {"sname": list_sname,
                      "num": list_num}
    dataFrame_all_stock = DataFrame(dict_all_stock)
    return codes, dataFrame_all_stock

if __name__ == '__main__':
    # codes, dataFrame = getCodes()
    #
    # 用DBAPI构建数据库链接engine
    engine = create_engine("mysql+mysqlconnector://root:1@localhost:3306/stock_classified?charset=utf8")
    # 建立连接
    con = engine.connect()

    # sql_read_stockCode = "select num from all_stock"
    # a = pd.read_sql(sql_read_stockCode, engine)
    # a_list = a['num'].tolist()


    file_dir = 'stock'

    i=0
    for file in os.listdir(file_dir):
        a_list_item = file.split('.')[0]
        if i > 499:
            print('股票' + a_list_item + ' 正在导入数据库。。。。。。')
            df = pd.read_csv('stock/'+ a_list_item +'.csv', encoding = 'gbk')
            if df.empty:
                print("df is empty")
            else:
                df.to_sql(name=a_list_item, con=con, if_exists='replace', index=True)
        i = i + 1