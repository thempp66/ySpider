# coding: utf-8

import requests
from bs4 import BeautifulSoup
import codecs
import redis


DOWNLOAD_URL = 'http://newcar.xcar.com.cn'
r = redis.Redis(host='localhost', port=6379, db=1)


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    request = requests.Session()
    request.proxies = {"http": "http://10.10.1.jdeoijf:3122/"}
    data = requests.get(url, headers=headers).content
    return data


def process_data(name, pql, gear, price):
    print name, pql, gear, price


def parse_html(html):
    soup = BeautifulSoup(html)
    car_blocks = soup.find_all('div', attrs={'class': 'xczx_cengmbox'})
    for car_block in car_blocks:
        car_lines = car_block.find_all('tr')
        for car_line in car_lines:
            if car_line.find('td', attrs={'class': 'bott'}) is not None:
                break
            car_infos = car_line.find_all('td')
            process_data(car_infos[0].find('a').getText(), car_infos[1].getText(), car_infos[2].getText(), car_infos[3].find('i').getText())
    tmp_str = soup.find_all('script', attrs={'language': 'javascript'})[-1].getText()
    tmp_str = tmp_str[tmp_str.find('(')+2: tmp_str.find(')')-1]
    soup2 = BeautifulSoup(tmp_str)
    next_page = soup2.find_all('a', attrs={'class': 'updowm'})[-1]['href']
    if next_page == 'javascript:;':
        return None
    else:
        return next_page


def main():
    url = "/car/6-0-0-0-0-0-7-0-0-0-0-0/"
    with codecs.open('cars','wb',encoding='utf-8') as fp:
        while url:
            html = download_page(DOWNLOAD_URL + url)
            url = parse_html(html)
            # fp.write(u'{cars}\n'.format(cars='\n'.join(cars)))

    member_set = r.smembers('2.0T')
    for member in member_set:
        print member

if __name__ == '__main__':
    main()