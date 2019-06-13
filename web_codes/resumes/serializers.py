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

    def get_candidate_id(self, resume):
        if resume.candidate:
            return resume.candidate.id
        else:
            return None

    def get_id(self, resume):
        return resume.id

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

        objs = Interview.objects.filter(post__pk=post_id, resume__pk=resume.id)
        if (objs):
            assert len(objs) == 1
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

    resume = ResumeSerializer(required=True)

    class Meta:
        model = Education
        fields = (
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
    def create(self, validated_data):
        resume_data = validated_data.pop('resume')
        resume = ResumeSerializer.create(ResumeSerializer(), validated_data=resume_data)

        education, created = Education.objects.update_or_create(
            resume=resume,**validated_data
        )
        return education
