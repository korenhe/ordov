# -*- coding:utf-8 -*-
#!/usr/bin/python

import json
import random
from faker import Faker
import requests
import os
ip="127.0.0.1"
url='http://127.0.0.1:8000/api/posts/'

def generate(i):
    with open("./post.template", "r", encoding='utf-8') as f:
        fake1 = Faker("zh_CN")
        payload = json.load(f)
        # update name
        payload['department']['company']['name'] = fake1.company()
        payload['department']['company']['short_name'] = fake1.company_prefix()
        payload['department']['company']['scale'] = random.randint(100, 100000)

        payload['address_province'] = fake1.province()
        payload['address_city'] = fake1.city()
        payload['address_district'] = fake1.district()
        payload['address_street'] = fake1.street_name()
        payload['address_suite'] = fake1.street_address()

        try:
            os.stat("pesudo_post")
        except:
            os.mkdir("pesudo_post")

        with open("pesudo_post/post.target.{}".format(i), "w", encoding='utf-8') as fw:
            json.dump(payload, fw, ensure_ascii=False)

NUM=100
if __name__ == '__main__':
    count = 0
    while (count < NUM):
        generate(count)
        count = count + 1
    i = 0

    while (i < NUM):
        cmd = "curl -X POST -H 'Content-type:application/json' 127.0.0.1:8000/api/posts/ -d@pesudo_post/post.target.{}".format(i)
        os.system(cmd)
        i = i+1
