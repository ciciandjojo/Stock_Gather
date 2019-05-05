# -*- coding: utf-8 -*-
"""
    @Time:2019/5/5 16:00
    @Author: John Ma
"""

import pymysql
import re
from sqlalchemy import create_engine
import pandas as pd

def table_exists(con, table_name):
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0

if __name__ == "__main__":
    connect = pymysql.connect(
        user='root',
        password='1',
        db='stock_classified',
        host='127.0.0.1',
        port=3306,
        charset='utf8'
    )
    con1 = connect.cursor()

    engine = create_engine("mysql+pymysql://root:1@localhost:3306/stock_classified?charset=utf8")
    # 建立连接
    con = engine.connect()

    sql_get_code = "select num from all_stock"
    all_stock = pd.read_sql_query(sql_get_code, con=engine)['num'].values.tolist()
    i = 0
    print(i)
    for stock in all_stock:
        i = i + 1
        if (table_exists(con1, stock) != 1):
            print(i)
