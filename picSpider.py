#-*- coding:utf-8 -*-
import re
import requests
import json
import time

DOWNLOAD_PAGE_BASE = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={input}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={input}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn={offset}&rn=30&gsm=1e&1513326191164='

def parse_html(html):
    content = html.content
    cJson = json.loads(content)
    imgList = cJson['data']
    cnt = 0
    for imgBlock in imgList:
        if imgBlock.has_key('middleURL'):
            print imgBlock['middleURL']
            cnt += 1
            with open('pics//{}.jpg'.format(int(round(time.time() * 1000))), 'wb') as fp:
                fp.write(requests.get(imgBlock['middleURL'], timeout=5).content)


def download_html(url):
    resp = requests.get(url)
    return resp


def main():
    page = 0
    while page <= 10:
        page += 1
        url = DOWNLOAD_PAGE_BASE.format(input='macan', offset=page*30)
        html = download_html(url)
        parse_html(html)


if __name__ == '__main__':
    main()