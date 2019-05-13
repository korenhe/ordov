from .resume_template import iPos
from resumes.models import Resume

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def update_language_info(resume, phone):
    lang_name = resume[iPos['LANGUAGE_NAME']].strip()
    lang_certification = resume[iPos['LANGUAGE_CERTIFICATION']]
    lang_description = resume[iPos['LANGUAGE_DESCRIPTION']].strip()

    try:
        resume = Resume.objects.get(phone_number=phone)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        print("Update Language: There Should Be One Resume Item, Return.")
        return

    lang = {
        "resume" : resume,
        "name" : lang_name,
        "cert" : lang_vertification,
        "description" : lang_description,
    }

    serializer = LanguageSerializer(data=lang)
    if serializer.is_valid(raise_exception=True):
        lang_saved = serializer.save()
    else:
        print("Fail to serilize language")

def update_certification_info(resume, phone):
    cert_name = resume[iPos['CERTIFICATION_NAME']].strip()
    cert_time = resume[iPos['CERTIFICATION_TIME']].strip()
    cert_institution = resume[iPos['CERTIFICATION_INSTITUTION']].strip()
    cert_description = resume[iPos['CERTIFICATION_DESCRIPTION']].strip()

    try:
        resume = Resume.objects.get(phone_number=phone)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        print("Update Certification: There Should Be One Resume Item, Return")
        return

    cert = {
        "resume" : resume,
        "time" : cert_time,
        "name" : cert_name,
        "institution" : cert_institution,
        "description" : cert_description,
    }

    serializer = CertificationSerializer(data=cert)
    if serializer.is_valid(raise_exception=True):
        cert_saved = serializer.save()
    else:
        print("Fail to serilize certification")
