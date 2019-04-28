# -*- coding:utf-8 -*-
#!/usr/bin/python
import json 
import random
from faker import Faker
import requests
import os
ip="127.0.0.1"
url='http://127.0.0.1:8001/api/resumes/'

dgreee=['高中', '硕士', '本科', '博士']

def generate(i):
    with open("./resume.template", "r") as f:
        fake1 = Faker("zh_CN")
        payload = json.load(f)
        # update name
        payload['resume']['username'] = fake1.name()
        # phone
        payload['resume']['phone_number'] = "+86"+fake1.phone_number()
        # qq
        qq =u''.join(str(random.choice(range(8))) for _ in range(8)) 
        payload['resume']['qq'] = long(qq)
        # identy
        payload['resume']['identity'] = fake1.ssn()
        # resident
        payload['resume']['residence'] = fake1.address().split()[0]
        payload['resume']['degree'] = dgreee[random.randint(0, len(dgreee)-1)]
        payload['resume']['birth_year'] = '2000'
        payload['resume']['email'] = fake1.free_email()

        with open("pesudo_resume/resume.target."+`i`, "w") as fw:
            json.dump(payload, fw)

        #resp = requests.post(url, headers={'Content-type':'application/json'}, data=payload)

if __name__ == '__main__':
    count = 0
    while (count < 100):
        generate(count)
        count = count + 1
    os.system("ls -al")
    i = 0 
    #curl -X POST -H 'Content-type:application/json' 127.0.0.1:8001/api/resumes/ -d@resume.template
    while (i < 100):       
        cmd = "curl -X POST -H 'Content-type:application/json' 127.0.0.1:8001/api/resumes/ -d@" + "pesudo_resume/resume.target."+`i`
        print cmd
        os.system(cmd)
        i = i+1
    os.system("rm pesudo_resume/*")
