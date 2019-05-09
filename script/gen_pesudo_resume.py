#!/usr/bin/env python


import json 
import random
from faker import Faker
import requests
import os
ip="127.0.0.1"
url='http://127.0.0.1:8000/api/resumes/'

degree_chocies=['高中', '硕士', '本科', '博士']
marriage_choices = ['未婚', '已婚', '离婚']

def generate(i):
    with open("./resume.template", "r", encoding='utf-8') as f:
        fake1 = Faker("zh_CN")
        payload = json.load(f)
        # update name
        payload['username'] = fake1.name()
        # phone
        payload['phone_number'] = "+86"+fake1.phone_number()
        # qq
        qq =u''.join(str(random.choice(range(8))) for _ in range(8))
        payload['qq'] = int(qq)
        # identy
        payload['identity'] = fake1.ssn()
        # resident
        payload['residence'] = fake1.address().split()[0]
        payload['degree'] = degree_chocies[random.randint(0, len(degree_chocies)-1)]
        payload['birth_year'] = '2000'
        payload['email'] = fake1.free_email()
        payload['marriage'] = marriage_choices[random.randint(0, len(marriage_choices)-1)]

        try:
            os.stat("pesudo_resume")
        except:
            os.mkdir("pesudo_resume")

        with open("pesudo_resume/resume.target.{}".format(i), "w", encoding='utf-8') as fw:
            json.dump(payload, fw, ensure_ascii=False)

        #resp = requests.post(url, headers={'Content-type':'application/json'}, data=payload)

NUM=100
if __name__ == '__main__':
    count = 0
    while (count < NUM):
        generate(count)
        count = count + 1
    i = 0

    while (i < NUM):
        cmd = "curl -X POST -H 'Content-type:application/json' 127.0.0.1:8000/api/resumes/ -d@pesudo_resume/resume.target.{}".format(i)
        print(cmd)
        os.system(cmd)
        i = i+1
    #os.system("rm pesudo_resume/*")
