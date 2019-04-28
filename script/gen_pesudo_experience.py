# -*- coding:utf-8 -*-
#!/usr/bin/python
import json 
import random
from faker import Faker
import requests
import os
ip="127.0.0.1"
url='http://127.0.0.1:8001/api/experiences/'


def generate(i):
    with open("./experience.template", "r") as f:
        fake1 = Faker("zh_CN")
        payload = json.load(f)
        # update name
        payload['experience']['witness'] = fake1.name()
        # phone
        payload['experience']['witness_phone'] = "+86"+fake1.phone_number()
        payload['experience']['company_name'] = fake1.company()
        payload['experience']['post_name'] = fake1.job()
        payload['experience']['resume'] = random.randint(0, 100)

        with open("pesudo_experience/experience.target."+`i`, "w") as fw:
            json.dump(payload, fw)

        #resp = requests.post(url, headers={'Content-type':'application/json'}, data=payload)

if __name__ == '__main__':
    count = 0
    while (count < 100):
        generate(count)
        count = count + 1
    os.system("ls -al")
    i = 0 
    #curl -X POST -H 'Content-type:application/json' 127.0.0.1:8001/api/experiences/ -d@experience.template
    while (i < 100):       
        cmd = "curl -X POST -H 'Content-type:application/json' 127.0.0.1:8001/api/experiences/ -d@" + "pesudo_experience/experience.target."+`i`
        print cmd
        os.system(cmd)
        i = i+1
    os.system("rm pesudo_experience/*")
