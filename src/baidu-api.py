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
FROM_LANG = cfg.get('baidu', 'fromLang')
TO_LANG = cfg.get('baidu', 'toLang')


class Query():
    def __get__(self, instance, owner):
       return self.q

    def __set__(self, instance, value):
        try:
            self.q = sys.argv[1]
        except:
            raise(ValueError, "Parameter error")


class Request:
    q = Query()
    def __init__(self, q):
        self.q = q
        self.fromLang = 'en'
        self.toLang = 'zh'

        self.m2 = hashlib.md5()
        self.m2.update(self.sign.encode("utf-8"))
        self.sign = self.m2.hexdigest()

    @property
    def url(self):
        extend_url = "?q={0}&from={1}&to={2}&appid={3}&salt={4}&sign={5}".format(self.q, self.fromLang, self.toLang, appid, self.salt, self.sign)
        return base_url + extend_url

    def request(self):
        response = requests.get(url=self.url)
        self.response = json.loads(response.text)
        sys.stdout.write('查询结果：' + self.response['trans_result'][0]['dst'] + '\n')

    def build_sign(self):

        self.salt = random.randint(32768, 65536)
        self.sign = APP_ID + self.q + str(self.salt) + SECRET_KEY

        return

if __name__ == '__main__':
    instance = Request(sys.argv)
    instance.request()
