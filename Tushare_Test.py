# -*- coding: utf-8 -*-
"""
    @Time:2019/4/8 11:45
    @Author: John Ma
"""

import tushare as ts
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd

# 行业分类
industry_classified = ts.get_industry_classified()

# # 概念分类
# concept_classified = ts.get_concept_classified()
#
# #地域分类
# area_classified = ts.get_area_classified()
#
# #中小板分类
# sme_classified = ts.get_sme_classified()
#
# #创业板分类
# gem_classified = ts.get_gem_classified()
#
# #风险警示板分类
# st_classified = ts.get_st_classified()
#
# # 沪深300成分及权重
# hs300 = ts.get_hs300s()
#
# #上证50成份股
# sz50s = ts.get_sz50s()
#
# # 中证500成份股
# zz500s = ts.get_zz500s()


# 用DBAPI构建数据库链接engine
engine = create_engine("mysql+mysqlconnector://root:1@localhost:3306/stock_classified?charset=utf8")
# 建立连接
con = engine.connect()
sql = "DROP TABLE IF EXISTS industry_classified"
sql2 = "DROP TABLE IF EXISTS industry"
engine.execute(sql2)
engine.execute(sql)
# industry_classified.to_sql(name='industry_classified', con=con, if_exists='replace',index=True)
num = 1
wocao =  pd.read_sql("SELECT * FROM `000001`", con=engine)

print(type(wocao))