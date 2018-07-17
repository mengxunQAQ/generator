import random
import hashlib
import requests
import json


appid = '20180717000186240'

secretKey = 'bjnInnIwET9ZsnpjsTaD'

base_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"

q = 'express'

fromLang = 'en'

toLang = 'zh'

salt = random.randint(32768, 65536)

sign = appid + q + str(salt) + secretKey

m2 = hashlib.md5()

m2.update(sign.encode("utf-8"))

sign = m2.hexdigest()

extend_url = "?q={0}&from={1}&to={2}&appid={3}&salt={4}&sign={5}".format(q, fromLang, toLang, appid, salt, sign)

rep = requests.get(url=base_url+extend_url)

print(rep.text)
print(json.loads(rep.text))