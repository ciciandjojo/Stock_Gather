# -*- coding: utf-8 -*-
"""
    @Time:2018/8/30 9:41
    @Author: John Ma
"""
import requests
import posixpath
from lxml import etree
import re

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

def parse_url(url):
    list = []
    response = requests.get(url,headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        html = etree.HTML(response.text)
        result = html.xpath('//tr//td/a')

        for i in range(len(result)):
            list.extend(re.findall(r"\d{6,10}",str(result[i].text)))
    # print(list)
    return list

if __name__ == '__main__':
    url = 'http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/3/ajax/1/code/881145'
    response_list = []
    for i in range(1,5):
        url = r'http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/' + str(i) + r'/ajax/1/code/881145'
        response = parse_url(url)
        response_list.extend(response)
    response_list.sort()
    f = open('Power.txt','w')
    for i in range(len(response_list)):
        f.write(response_list[i])
        if i != len(response_list)-1 :
            f.write('\n')