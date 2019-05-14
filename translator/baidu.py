import sys
import os
import random
import hashlib
import json
import argparse

import requests

from configparser import ConfigParser

sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")))

cfg = ConfigParser()
cfg.read(r'../conf.ini')
APP_ID = cfg.get('baidu', 'app_id')
SECRET_KEY = cfg.get('baidu', 'secret_key')
BASE_URL = cfg.get('baidu', 'base_url')
FROM_LANG = cfg.get('language', 'fromLang')
TO_LANG = cfg.get('language', 'toLang')


class Request:
    def __init__(self, query):
        self.query = query
        self.sign, self.salt = self.generate_sign()

    @property
    def url(self):
        """
        joint url between base-url and extend-url
        """
        extend_url = "?q={0}&from={1}&to={2}&appid={3}&salt={4}&sign={5}".format(self.query, FROM_LANG, TO_LANG, APP_ID, self.salt, self.sign)
        return BASE_URL + extend_url

    def request(self):
        """
        request to http://api.fanyi.baidu.com for result
        """
        return requests.get(url=self.url)

    def response(self):
        """
        get response
        """
        response = self.request()
        return json.loads(response.text)

    def output(self):
        """
        print result
        """
        response = self.response()
        if response.get("trans_result"):
            sys.stdout.write(response["trans_result"][0]["dst"])
        else:
            sys.stdout.write("error")

    def generate_sign(self):
        """
        generate sign and salt
        """
        salt = random.randint(32768, 65536)
        sign = APP_ID + self.query + str(salt) + SECRET_KEY
        m2 = hashlib.md5()
        m2.update(sign.encode("utf-8"))
        sign_md5 = m2.hexdigest()

        return sign_md5, salt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str, help="input an English word")
    args = parser.parse_args()
    word = args.word

    result = Request(word)
    result.output()
