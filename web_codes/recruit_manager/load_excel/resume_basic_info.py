from .resume_template import iPos
from resumes.models import Resume
from resumes.serializers import ResumeSerializer
import json

def create_or_update_basic_info(resume):

    # step1: get basic info from resume
    name = resume[iPos['PHONE']].strip()
    resume_way = resume[iPos['RESUME_WAY']].strip()
    resume_way2 = resume[iPos['RESUME_WAY2']].strip()
    user = resume[iPos['NAME']].strip()
    phone = resume[iPos['PHONE']].strip()
    gender = resume[iPos['GENDER']].strip()
    qq = resume[iPos['QQ']]
    email = resume[iPos['EMAIL']].strip()

    birth_year = resume[iPos['BIRTH_YEAR']]
    birth_month = resume[iPos['BIRTH_MONTH']]
    birth_day = resume[iPos['BIRTH_DAY']]
    identity = resume[iPos['IDENTITY']].strip()

    degree = resume[iPos['DEGREE']].strip()
    major = resume[iPos['MAJOR']].strip()
    school = resume[iPos['SCHOOL']].strip()
    graduate_time = resume[iPos['GRADUATE_TIME']].strip()
    live_stat = resume[iPos['LIVE_STATE']].strip()
    self_description = resume[iPos['SELF_DESCRIPTION']].strip()

    birth_province = resume[iPos['BIRTH_PLACE_PROVINCE']].strip()
    birth_city= resume[iPos['BIRTH_PLACE_CITY']].strip()
    birth_district = resume[iPos['BIRTH_PLACE_DISTRICT']].strip()
    birth_place = resume[iPos['BIRTH_PLACE_STREET']].strip()

    current_settle_province = resume[iPos['CURRENT_SETTLE_PROVINCE']]
    current_settle_city = resume[iPos['CURRENT_SETTLE_CITY']]
    current_settle_district = resume[iPos['CURRENT_SETTLE_DISTRICT']]
    current_settle_street = resume[iPos['CURRENT_SETTLE_STREET']]
    marriage = resume[iPos['MARRIAGE']].strip()

    # step2: preDeal the basic info
    if gender == '男':
        gender = 'm'
    else:
        gender = 'f'

    if not birth_year == '':
        birth_year = int(birth_year)
    if not birth_month == '':
        birth_month = int(birth_month)
    if not birth_day == '':
        birth_day = int(birth_day)

    # step3: create the basic info
    resume = {
		"candidate": {},
		"resume_id" : 1,
		"visible" : False,
		"resume_way" : resume_way,
		"resume_way2" : resume_way2,
		"username" : user,

		"gender" : gender,
		"phone" : "+86" + phone,
		"birth_year" : birth_year,
		"birth_month" : birth_month,
		"birth_day" : birth_day,
		"identity" : identity,

		"degree" : degree,
		"major" : major,
		"school" : school,

		"graduate_time" : graduate_time,
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
    else:
        print("Fail to seriliaze resume")