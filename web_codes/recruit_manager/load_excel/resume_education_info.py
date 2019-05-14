from .resume_template import iPos
from resumes.models import Resume
from resumes.models import Education

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from resumes.serializers import EducationSerializer


def update_education_info(resume, phone):
    if phone is "":
        return
    # step1: get raw data
    edu_start = resume[iPos['EDUCATION_START_TIME']].strip()
    edu_end = resume[iPos['EDUCATION_END_TIME']].strip()
    edu_school = resume[iPos['EDUCATION_SCHOOL']].strip()
    edu_colleage = resume[iPos['EDUCATION_COLLEGE']].strip()
    edu_major = resume[iPos['EDUCATION_MAJOR']].strip()
    edu_type = resume[iPos['EDUCATION_TYPE']].strip()
    edu_degree = resume[iPos['EDUCATION_DEGREE']].strip()
    edu_reference = resume[iPos['EDUCATION_REFERENCE']].strip()
    edu_reference_phone = resume[iPos['EDUCATION_REFERENCE_PHONE']].strip()
    edu_provice = resume[iPos['EDUCATION_PROVICE']].strip()
    edu_city = resume[iPos['EDUCATION_CITY']].strip()
    edu_district = resume[iPos['EDUCATION_DISTRICT']].strip()
    edu_street = resume[iPos['EDUCATION_STREET']].strip()

    # step2: refresh data
    print("edu_start", edu_start)
    edu_start = edu_start + "-01"
    print("edu_end", edu_end)
    edu_end = edu_end +"-01"
    # step3: create education info

    resumeTarget = None
    try:
        resumeTarget = Resume.objects.get(phone_number=phone)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        print("Update Education: There Should Be One Resume, Return")
        return

    education = {
        "resume" : resumeTarget,
        "start" : edu_start,
        "end" : edu_end,

        "school" : edu_school,
        "college" : edu_colleage,
        "major" : edu_major,
        "degree" : edu_degree,
        "edu_type" : edu_type,

        "province" : edu_provice,
        "city" : edu_city,
        "district" : edu_district,
        "street" : edu_street,
        "place" : edu_provice + edu_city + edu_district + edu_street,

        "instructor" : edu_reference,
        "instructor_phone" : edu_reference_phone,
    }

    serializer = EducationSerializer(data=education)
    if serializer.is_valid(raise_exception=True):
        education_saved = serializer.save()
    else:
        print("Fail to serilize education")
