# -*- coding: utf-8 -*-
"""
    @Time:2018/8/27 17:49
    @Author: John Ma
"""
import requests
import pandas as pd
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

def parse_url(url):
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return etree.HTML(response.content)
    return False

def get_date(response):
    # 得到股票代码，开始和结束的日期
    start_date = ''.join(response.xpath('//input[@name="date_start_type"]/@value')[0].split('-'))
    end_date = ''.join(response.xpath('//input[@name="date_end_type"]/@value')[0].split('-'))
    code = response.xpath('//h1[@class="name"]/span/a/text()')[0]
    return code,start_date,end_date

def download(code,start_date, end_date):
    download_url = "http://quotes.money.163.com/service/chddata.html?code=1"+code+"&start="+start_date+"&end="+end_date+\
    "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
    print(download_url)
    data = requests.get(download_url,headers=headers)
    f = open(code + '.csv', 'wb')
    for chunk in data.iter_content(chunk_size=10000):
        if chunk:
            f.write(chunk)
    print('股票---',code,'历史数据正在下载')

if __name__ == '__main__':
    url = 'http://quotes.money.163.com/trade/lsjysj_002230.html'
    response = parse_url(url)
    code,start_date,end_date = get_date(response)
    download(code,start_date, end_date)

    stock = pd.read_csv(code + '.csv', usecols=[0, 1, 2, 3, 4, 5, 6], encoding='gbk')
    stock_new = stock.iloc[:180, :]
    stock_new_sorted = stock_new.sort_values('日期', ascending=True)


    print(stock_new_sorted.head())

    from pyecharts import Kline

    stock_code = stock_new_sorted['股票代码'][0]
    stock_name = stock_new_sorted['名称'][0]
    index = stock_new_sorted['日期']
    v = [[o, close, lowest, highest] for o, close, lowest, highest in
         zip(stock_new_sorted['开盘价'], stock_new_sorted['收盘价'], stock_new_sorted['最低价'], stock_new_sorted['最高价'])]
    kline = Kline()
    kline.add(stock_name + '(' + stock_code + ')' + '日K线图', index, v, mark_point=["max"], is_datazoom_show=True)

    from pyecharts import Line

    line = Line(stock_name + '(' + stock_code + ')' + '收盘价日折线图')
    close = stock_new_sorted['收盘价']
    line.add("收盘价日折线图", index, close, is_datazoom_show=True)
    line.render()

    from pyecharts import Kline, Line, Overlap

    overlap = Overlap()
    overlap.add(kline)
    overlap.add(line)
    overlap.render()