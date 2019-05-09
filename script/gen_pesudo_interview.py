# -*- coding:utf-8 -*-
#!/usr/bin/python
import json
import random
from faker import Faker
import requests
import os
ip="127.0.0.1"
url='http://127.0.0.1:8000/api/interviews/'

def generate(i):
    with open("./interview.template", "r", encoding='utf-8') as f:
        fake1 = Faker("zh_CN")
        payload = json.load(f)

        payload['post'] = random.randint(0, 100)

        payload['is_active'] = fake1.boolean()
        payload['status'] = random.randint(0, 6)

        try:
            os.stat("pesudo_interview")
        except:
            os.mkdir("pesudo_interview")

        with open("pesudo_interview/interview.target.{}".format(i), "w", encoding='utf-8') as fw:
            json.dump(payload, fw, ensure_ascii=False)

NUM=20
if __name__ == '__main__':
    count = 0
    while (count < NUM):
        generate(count)
        count = count + 1

    i = 0

    while (i < NUM):
        cmd = "curl -X POST -H 'Content-type:application/json' 127.0.0.1:8000/api/interviews/ -d@pesudo_interview/interview.target.{}".format(i)
        os.system(cmd)
        i = i+1
