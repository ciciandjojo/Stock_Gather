# -*- coding: utf-8 -*-
"""
    @Time:2018/8/27 17:02
    @Author: John Ma
"""
#  在网易财经中下载水泥行业及其上游行业的股票信息
import requests
from lxml import etree
import os
import time

import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

# 获取需要爬出股票网页的信息
def parse_url(url):
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return etree.HTML(response.content)
    return False

#  获取该股票的开始与现在的时间还有名字
def get_date(response):
    # 得到股票代码，开始和结束的日期
    start_date = ''.join(response.xpath('//input[@name="date_start_type"]/@value')[0].split('-'))
    end_date = ''.join(response.xpath('//input[@name="date_end_type"]/@value')[0].split('-'))
    code = response.xpath('//h1[@class="name"]/span/a/text()')[0]
    return code,start_date,end_date

# 将以上信息做一个整合通过获取下载来获取到本地
def download(file_url,code,start_date, end_date):
    if str(code).startswith('6') or str(code).startswith('9'):
        download_url = "http://quotes.money.163.com/service/chddata.html?code=0" + code + "&start=" + start_date + "&end=" + end_date + \
                       "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        print(download_url)
        data = requests.get(download_url, headers=headers)
        f = open(file_url + code + '.csv', 'wb')
        for chunk in data.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
        print('股票---', code, '历史数据正在下载')
    else:
        download_url = "http://quotes.money.163.com/service/chddata.html?code=1"+code+"&start="+start_date+"&end="+end_date+\
                       "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        # print(download_url)
        data = requests.get(download_url,headers=headers)
        f = open(file_url + code + '.csv', 'wb')
        for chunk in data.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
        print('股票---',code,'历史数据正在下载')

# 删除某一类混合到另外一类信息的文件
def delete(url):
    my_file = 'stock_data//'
    url = my_file + url + r'.csv'
    if os.path.exists(url):
        os.remove(url)
    else:
        print('no such file:%s' % url)

if __name__ == '__main__':

    # 22只水泥行业股票
    stock_num_list_cement = ['000401', '000546', '000672', '000789', '000877',
                             '000885', '000935', '002233', '600068', '600318',
                             '600326', '600425', '600449', '600539', '600585',
                             '600668', '600678', '600720', '600801', '600802',
                             '600881', '601992']

    # 19只航运股票
    stock_num_list_navigation = ['000039', '000507', '000520', '002320', '002401', '002685',
                                 '600026', '600242', '600260', '600428', '600688', '600751',
                                 '600798', '601228', '601866', '601872', '601919', '603167',
                                 '603869']

    open_stock = open('real_estate_stockNumber.txt', 'r')   # 142只房地产的股票
    open_stock_Power = open('Power_stockNumber.txt', 'r')   # 73只电力股票
    open_stock_EC = open('engineering_construction_stockNumber.txt','r')    # 76只工程建设的股票

    stock_num_list_real_estate = open_stock.read().split('\n')
    stock_num_list_real_estate.sort()
    stock_num_list_power = open_stock_Power.read().split('\n')
    stock_num_list_power.sort()
    stock_num_list_EC = open_stock_EC.read().split('\n')
    stock_num_list_EC.sort()

    # test
    # url = 'http://quotes.money.163.com/trade/lsjysj_837822.html'

    file_url = 'stock_data/RealEstate/'
    for stock_num in stock_num_list_real_estate:
        #循环输出我想要的股票的数据
        url = 'http://quotes.money.163.com/trade/lsjysj_' + stock_num + '.html'
        response = parse_url(url)
        code,start_date,end_date = get_date(response)
        download(file_url, code, start_date, end_date)
    # delete(stock_num)
    # print(response)