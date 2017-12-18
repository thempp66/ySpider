import time
import requests
from bs4 import BeautifulSoup


def kill_captcha(data):
    with open('captcha.png', 'wb') as fp:
        fp.write(data)
    return raw_input('captcha : ')


def login(username, password, oncaptcha):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    session = requests.session()
    _xsrf = BeautifulSoup(session.get('https://www.zhihu.com/#signin', headers=headers).content).find('input', attrs={
        'name': '_xsrf'})['value']
    captcha_content = session.get('http://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn' % (time.time() * 1000)).content
    data = {
        '_xsrf': _xsrf,
        'password': password,
        'captcha_type': 'cn',
        'phone_num': username
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'X-Xsrftoken':_xsrf
    }
    requests.headers = headers
    response = session.post('https://www.zhihu.com/login/phone_num', data).content
    return session


if __name__ == '__main__':
    session = login('18889898688', 'qa781890', kill_captcha)
    print BeautifulSoup(session.get("https://www.zhihu.com").content).find('span', class_='name').getText()
