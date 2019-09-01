from rest_framework import serializers

from candidates.serializers import CandidateSerializer
from .models import Resume, Education
from interviews.models import Interview, STATUS_CHOICES

class ResumeSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(required=False)
    candidate_id = serializers.SerializerMethodField()
    interview_id = serializers.SerializerMethodField()
    interview_status = serializers.SerializerMethodField()
    interview_status_name = serializers.SerializerMethodField()
    workexp = serializers.SerializerMethodField()
    ageg = serializers.SerializerMethodField()
    newname = serializers.SerializerMethodField()
    birthorigin = serializers.SerializerMethodField()
    expected = serializers.SerializerMethodField()

    def get_candidate_id(self, resume):
        if resume.candidate:
            return resume.candidate.id
        else:
            return None

    def get_id(self, resume):
        return resume.id

    def get_ageg(self, resume):
        return "年龄:" + str(resume.age)+" " "毕业: "+str(resume.graduate_time)
    def get_newname(self, resume):
        if resume.gender == "Male":
            return resume.username
        elif resume.gender == "Female":
            return resume.username+"(女)"
        else:
            return resume.username
    def get_expected(self, resume):
        #TODO: expected city and more
        if resume.expected_city is not None:
            return "期望地点:"+resume.expected_city
        else:
            return "--"
    def get_birthorigin(self, resume):
        birth =""
        hasBirthInfo = False
        if resume.birth_province is not None:
            birth = birth + resume.birth_province
            hasBirthInfo = True
        if resume.birth_city is not None:
            birth = birth + "." + resume.birth_city
            hasBirthInfo = True
        if resume.birth_district is not None:
            birth = birth + "." + resume.birth_district
            hasBirthInfo = True
        if hasBirthInfo is False:
            return "无籍贯信息"
        return birth

    # by post id, can be is_in_interview for post1 but not for post2
    def get_workexp(self, resume):
        resume = Resume.objects.get(pk=resume.id)
        exps = resume.experience_set.all()

        if exps:
            expression = '</br>'.join([str(exp) for exp in exps])
            return expression
        else:
            return "--"

    def get_interview_id(self, resume):
        post_id = self.context.get('post_id')

        objs = Interview.objects.filter(post__pk=post_id, resume__pk=resume.id)
        if (objs):
            return objs[0].id
        else:
            return None

    def get_interview_status(self, resume):
        post_id = self.context.get('post_id')

        objs = Interview.objects.filter(post__pk=post_id, resume__pk=resume.id)
        if (objs):
            assert len(objs) == 1
            return objs[0].status
        else:
            # default 0
            return 0

    def get_interview_status_name(self, resume):
        post_id = self.context.get('post_id')

        # status_name such a complicated issue
        statusId = -1
        objsStatusId = Interview.objects.filter(post__pk=post_id, resume__pk=resume.id)
        if (objsStatusId):
            statusId = int(objsStatusId[0].status)

        objs = Interview.objects.filter(post__pk=post_id, resume__pk=resume.id)
        if (objs):
            assert len(objs) == 1
            # check the status
            if statusId == 3:
                appointmentObjs = objs[0].interviewsub_appointment_set.all()
                assert len(appointmentObjs) == 1
                agreeObjs = appointmentObjs[0].interviewsub_appointment_agree_set.all()
                assert len(agreeObjs) == 1
                if agreeObjs[0].date is None:
                    return "无该同学面试时间信息"
                else:
                    return "约定面试: "+agreeObjs[0].date.strftime("%Y/%m/%d %H:%M:%S")
                # the interview status, we should show the interview time
            elif statusId == 4:
                offerObjs = objs[0].interviewsub_offer_set.all()
                if len(offerObjs) < 1:
                    return "请填写offer信息"
                offerAgreeObjs = offerObjs[0].interviewsub_offer_agree_set.all()
                if len(offerAgreeObjs) < 1:
                    return "请填写offer信息"
                if offerAgreeObjs[0].date is None:
                    return "请填写offer入职时间信息"
                else:
                    return "预期入职: " + offerAgreeObjs[0].date.strftime("%Y/%m/%d %H:%M:%S")
            elif statusId == 5:
                offerObjs = objs[0].interviewsub_offer_set.all()
                if len(offerObjs) < 1:
                    return "无该同学offer信息"
                offerAgreeObjs = offerObjs[0].interviewsub_offer_agree_set.all()
                if len(offerAgreeObjs) < 1:
                    return "无该同学offer信息"
                if offerAgreeObjs[0].date is None:
                    return "无该同学入职时间信息"
                else:
                    return "预期入职: " + offerAgreeObjs[0].date.strftime("%Y/%m/%d %H:%M:%S")
            else:
                return objs[0].sub_status
        else:
            # default 0
            return "--"

    class Meta:
        model = Resume
        fields = (
            # MethodField

            'interview_id',
            'candidate_id',
            'id',
            'interview_status',
            'interview_status_name',
            'workexp',
            'ageg',
            'newname',
            'birthorigin',
            'expected',

            # CascadeField
            'candidate',

            # OrdinaryField

            'resume_id',
            'visible',
            'username',
            'gender',
            'birth_year',
            'birth_month',
            'date_of_birth',
            'identity',
            'age',

            'phone_number',
            'qq',
            'residence',
            'email',
            'marriage',

            'degree',
            'major',
            'school',

            'birth_province',
            'birth_city',
            'birth_district',

            'expected_province',
            'expected_city',
            'expected_district',

            'graduate_time',
            'graduate_year',

        )

    def create(self, validated_data):
#        try:
#            candidate_data = validated_data.pop('candidate')
#            candidate = CandidateSerializer.create(CandidateSerializer(), validated_data=candidate_data)

#            resume, created = Resume.objects.update_or_create(
#                candidate=candidate, **validated_data)
#            return resume
#        except KeyError:

#            resume = Resume.objects.create(**validated_data)
#            return resume

        # create resume, currently we use the phone as key to identify one resume
        resumeTarget = None
        try:
            phone=validated_data['phone_number']
            if phone == '':
                return None
            resumeTarget = Resume.objects.get(phone_number=phone)
        except:
            pass
        if resumeTarget is None:
            candidate_data = validated_data.pop('candidate')
            resume = Resume.objects.create(**validated_data)
            return resume
        else:
            return resumeTarget

class EducationSerializer(serializers.ModelSerializer):

    # DO NOT WRAP EMBEDDED FOREIGN KEY OBJECT HERE
    # REFER TO: ExperienceSerializer
    class Meta:
        model = Education
        fields = (
            'id',
            'resume', # foreginkey
            'start',
            'end',
            'school',
            'college',
            'major',
            'degree',
            'edu_type',
            'province',
            'city',
            'district',
            'street',
            'place',
            'instructor',
            'instructor_phone',
        )
