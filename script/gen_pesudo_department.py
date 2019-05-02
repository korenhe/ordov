# -*- coding:utf-8 -*-
#!/usr/bin/python
import json
import random
from faker import Faker
import requests
import os
ip="127.0.0.1"
url='http://127.0.0.1:8001/api/departments/'


def generate(i):
    with open("./department.template", "r") as f:
        fake1 = Faker("zh_CN")
        payload = json.load(f)
        # update name
        payload['department']['name'] = fake1.department()
        payload['department']['short_name'] = fake1.department_prefix()
        payload['department']['scale'] = random.randint(100, 100000)
        payload['department']['description'] =  payload['department']['name'] + payload['department']['short_name']

        try:
            os.stat("pesudo_department")
        except:
            os.mkdir("pesudo_department")

        with open("pesudo_department/department.target.{}".format(i), "w") as fw:
            json.dump(payload, fw)

        #resp = requests.post(url, headers={'Content-type':'application/json'}, data=payload)

if __name__ == '__main__':
    count = 0
    while (count < 100):
        generate(count)
        count = count + 1
    os.system("ls -al")
    i = 0
    #curl -X POST -H 'Content-type:application/json' 127.0.0.1:8001/api/departments/ -d@department.template
    while (i < 100):
        cmd = "curl -X POST -H 'Content-type:application/json' 127.0.0.1:8000/api// -d@" + "pesudo_department/department.target.{}".format(i)
        print(cmd)
        os.system(cmd)
        i = i+1
    os.system("rm pesudo_department/*")
