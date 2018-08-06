import sys
import os
import random
import hashlib
import requests
import json

from configparser import ConfigParser

sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")))


cfg = ConfigParser()
cfg.read(r'../conf.ini')
APP_ID = cfg.get('baidu', 'app_id')
SECRET_KEY = cfg.get('baidu', 'secret_key')
BASE_URL = cfg.get('baidu', 'base_url')
FROM_LANG = cfg.get('language', 'fromLang')
TO_LANG = cfg.get('language', 'toLang')


class Query():
    def __get__(self, instance, owner):
       return self.query

    def __set__(self, instance, value):
        try:
            self.query = sys.argv[1]
        except:
            raise(ValueError, "Parameter error")


class Request:

    query = Query()
    def __init__(self, query):

        self.query = query
        self.sign = self.build_sign()

    @property
    def url(self):
        extend_url = "?q={0}&from={1}&to={2}&appid={3}&salt={4}&sign={5}".format(self.query, FROM_LANG, TO_LANG, APP_ID, self.salt, self.sign)
        return BASE_URL + extend_url

    def request(self):
        return requests.get(url=self.url)

    def response(self):
        response = self.request()
        return json.loads(response.text)

    def output(self):
        response = self.response()
        sys.stdout.write('\033[0;31m查询结果：' + response['trans_result'][0]['dst'] + '\033[0m\n')

    def build_sign(self):
        self.salt = random.randint(32768, 65536)
        self.sign = APP_ID + self.query + str(self.salt) + SECRET_KEY
        self.m2 = hashlib.md5()
        self.m2.update(self.sign.encode("utf-8"))
        self.sign = self.m2.hexdigest()

        return self.sign


if __name__ == '__main__':
    instance = Request(sys.argv)
    instance.output()
