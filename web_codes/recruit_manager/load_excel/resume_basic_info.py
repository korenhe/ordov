#-*- coding:utf-8 -*-
from .resume_template import iPos
from resumes.models import Resume
from resumes.serializers import ResumeSerializer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .common import validate_degree

import json

def create_or_update_basic_info(resume, phone):

    user = resume[iPos['NAME']].strip()
    phone = str(resume[iPos['PHONE']]).strip()

    # step0: check if the phone is registered
    # For resumes from excel, we regard phone_number as 'primary key'

    resumeTarget = None
    try:
        resumeTarget = Resume.objects.get(phone_number=phone, username=user)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        pass

    if not resumeTarget is None:
        #print(json.dumps(resumeTarget, ensure_ascii=False))
        return False

    print("No Item for", phone, ", Create it")
    # step1: get basic info from resume
    resume_way = str(resume[iPos['RESUME_WAY']]).strip()
    resume_way2 = str(resume[iPos['RESUME_WAY2']]).strip()
    gender = str(resume[iPos['GENDER']]).strip()
    qq = resume[iPos['QQ']]
    email = str(resume[iPos['EMAIL']]).strip()

    birth_year = resume[iPos['BIRTH_YEAR']]
    birth_month = resume[iPos['BIRTH_MONTH']]
    birth_day = resume[iPos['BIRTH_DAY']]
    identity = str(resume[iPos['IDENTITY']]).strip()

    degree = str(resume[iPos['DEGREE']]).strip()
    major = str(resume[iPos['MAJOR']]).strip()
    school = str(resume[iPos['SCHOOL']]).strip()
    graduate_time = str(resume[iPos['GRADUATE_TIME']]).strip()
    live_stat = str(resume[iPos['LIVE_STATE']]).strip()
    self_description = str(resume[iPos['SELF_DESCRIPTION']]).strip()

    birth_province = str(resume[iPos['BIRTH_PLACE_PROVINCE']]).strip()
    birth_city= str(resume[iPos['BIRTH_PLACE_CITY']]).strip()
    birth_district = str(resume[iPos['BIRTH_PLACE_DISTRICT']]).strip()
    birth_place = str(resume[iPos['BIRTH_PLACE_STREET']]).strip()

    current_settle_province = resume[iPos['CURRENT_SETTLE_PROVINCE']]
    current_settle_city = resume[iPos['CURRENT_SETTLE_CITY']]
    current_settle_district = resume[iPos['CURRENT_SETTLE_DISTRICT']]
    current_settle_street = resume[iPos['CURRENT_SETTLE_STREET']]
    marriage = str(resume[iPos['MARRIAGE']].strip())
    # TODO FIX
    marriage = "已婚"
    ageStr = str(resume[iPos['AGE']])

    # step2: preDeal the basic info
    if gender == '男':
        gender = 'm'
    else:
        gender = 'f'

    degreeNO = validate_degree(degree)

    age = 0
    if not age == '':
        age = int(float(ageStr))
    if not birth_month == '':
        birth_month = int(birth_month)
    if not birth_day == '':
        birth_day = int(birth_day)

    graduate_time = "1980-03-23"
    graduate_year = 1988

    # step3: create the basic info
    resume = {
		"candidate": {},
		"resume_id" : 1,
		"visible" : False,
		"resume_way" : resume_way,
		"resume_way2" : resume_way2,
		"username" : user,

		"gender" : gender,
		"phone_number" : phone,
		"birth_year" : birth_year,
		"birth_month" : birth_month,
		"birth_day" : birth_day,
		"identity" : identity,
        "email": email,
        "age": age,

		"degree" : degreeNO,
		"major" : major,
		"school" : school,

		"graduate_time" : graduate_time,
        "graduate_year" : graduate_year,
		"live_state" : live_stat,
		"self_description" : self_description,

		"birth_province" : birth_province,
		"birth_city" : birth_city,
		"birth_district" : birth_district,

		"current_settle_provice" : current_settle_province,
		"current_settle_city" : current_settle_city,
		"current_settle_district" : current_settle_district,
		"current_settle_street" : current_settle_street,

		"marriage" : marriage,
    }


    serializer = ResumeSerializer(data=resume)
    if serializer.is_valid(raise_exception=True):
        resume_saved = serializer.save()
        print("resume update done", resume_saved)
    else:
        print("Fail to seriliaze resume")

    return True
