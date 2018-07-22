import sys
import os
import random
import hashlib
import requests
import json


sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")))

from conf.baidu import APP_id as appid, SECRET_KEY as secretKey, BASE_URL as base_url

# appid = '20180717000186240'
#
# secretKey = 'bjnInnIwET9ZsnpjsTaD'
#
# base_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"


class Query():
    def __get__(self, instance, owner):
       return self.q

    def __set__(self, instance, value):
        try:
            self.q = sys.argv[1]
        except:
            raise ValueError


class API:
    q = Query()
    def __init__(self, q):
        self.q = q
        self.fromLang = 'auto'
        self.toLang = 'zh'
        self.salt = random.randint(32768, 65536)
        self.sign = appid + self.q + str(self.salt) + secretKey
        self.m2 = hashlib.md5()
        self.m2.update(self.sign.encode("utf-8"))
        self.sign = self.m2.hexdigest()

    @property
    def url(self):
        extend_url = "?q={0}&from={1}&to={2}&appid={3}&salt={4}&sign={5}".format(self.q, self.fromLang, self.toLang, appid, self.salt, self.sign)
        return base_url + extend_url

    def request(self):
        rep = requests.get(url=self.url)
        return json.loads(rep.text).get('trans_result')

    def __repr__(self):
        rep = self.request()
        if not rep:
            raise ValueError("error")  # todo: error message
        return "result: %s"%(rep[0].get('dst'))  # todo: en --> zh, zh --> en


if __name__ == '__main__':
    instance = API(sys.argv)
    print(instance)
