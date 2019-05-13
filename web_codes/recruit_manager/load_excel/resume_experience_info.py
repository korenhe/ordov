from .resume_template import iPos
from resumes.models import Resume

from experiences.serializers import ExperienceSerializer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def update_experience_info(resume, phone):

    # step1: get the raw data
    exp_start = resume[iPos['EXPERIENCE_START_TIME']].strip()
    exp_end = resume[iPos['EXPERIENCE_END_TIME']].strip()
    exp_company = resume[iPos['EXPERIENCE_COMPANY_NAME']].strip()
    exp_company_short = resume[iPos['EXPERIENCE_COMPANY_SHORT_NAME']].strip()
    exp_department = resume[iPos['EXPERIENCE_DEPARTMENT']].strip()
    exp_post_name = resume[iPos['EXPERIENCE_POST_NAME']].strip()
    exp_post_class = resume[iPos['EXPERIENCE_POST_CLASS']].strip()
    exp_post_type = resume[iPos['EXPERIENCE_POST_TYPE']].strip()
    exp_post_rank = resume[iPos['EXPERIENCE_POST_RANK']].strip()
    exp_post_feature = resume[iPos['EXPERIENCE_POST_FEATURE']].strip()
    exp_post_subornates = resume[iPos['EXPERIENCE_POST_SUBORNATES']]
    exp_post_duty = resume[iPos['EXPERIENCE_POST_DUTY']].strip()
    exp_post_summary = resume[iPos['EXPERIENCE_POST_SUMMARY']].strip()
    exp_post_base_salary = resume[iPos['EXPERIENCE_POST_BASE_SALARY']].strip()
    exp_post_deduct_salary = resume[iPos['EXPERIENCE_POST_DEDUCT_SALARY']].strip()
    exp_post_zuoxi = resume[iPos['EXPERIENCE_POST_ZUOXI']].strip()
    exp_post_leave_reason = resume[iPos['EXPERIENCE_POST_LEAVE_REASON']].strip()
    exp_post_provice = resume[iPos['EXPERIENCE_POST_PROVICE']].strip()
    exp_post_city = resume[iPos['EXPERIENCE_POST_CITY']].strip()
    exp_post_district = resume[iPos['EXPERIENCE_POST_DISTRICT']].strip()

    exp_post_reference = resume[iPos['EXPERIENCE_POST_REFERENCE']].strip()
    exp_post_reference_post = resume[iPos['EXPERIENCE_POST_REFERENCE_POST']].strip()
    exp_post_reference_phone = resume[iPos['EXPERIENCE_POST_REFERENCE_PHONE']].strip()

    # step2: refresh data
    # step3: create experience data
    try:
        resume = Resume.objects.get(phone_number=phone)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        print("Update Experience: There Should Be One Resume, Return")
        return

    experience = {
        "resume" : resume,
        "start" : exp_start,
        "end" : exp_end,
        "company_name" : exp_company,
        "department_name" : exp_department,
        "post_name" : exp_post_name,

        "pType" : exp_post_type,
        "pFeature" : exp_post_feature,

        "subornates" : exp_post_subornates,
        "level" : exp_post_rank,
        "duty" : exp_post_duty,
        "salary" : exp_post_base_salary,
        "deduct_salary" : exp_post_deduct_salary,

        "shift" : exp_post_zuoxi,
        "leave_reason" : exp_post_leave_reson,

        "work_province" : exp_post_provice,
        "work_city" : exp_post_city,
        "work_district" : exp_post_district,

        "witness" : exp_post_reference,
        "witness_post" : exp_post_reference_post,
        "witness_phone" : exp_post_reference_phone,
    }

    serializer = ExperienceSerializer(data=experience)
    if serializer.is_valid(raise_exception=True):
        experience_saved = serializer.save()
    else:
        print("Fail to serilize experience")
