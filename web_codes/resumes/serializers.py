from rest_framework import serializers

from candidates.serializers import CandidateSerializer
from .models import Resume, Education
from interviews.models import Interview

class ResumeSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(required=False)
    candidate_id = serializers.SerializerMethodField()
    is_in_interview = serializers.SerializerMethodField()

    def get_candidate_id(self, resume):
        if resume.candidate:
            return resume.candidate.id
        else:
            return None

    def get_id(self, resume):
        return resume.id

    def get_is_in_interview(self, resume):
        post_id = self.context.get('post_id')

        if (Interview.objects.filter(post__pk=post_id, resume__pk=resume.id)):
            print("in interview", post_id)
            return True
        else:
            print("not in interview", post_id)
            return False

    class Meta:
        model = Resume
        fields = (
            # MethodField

            'candidate_id',
            'id',
            'is_in_interview',

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
        )

    def create(self, validated_data):
#        try:
#            print(validated_data)
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
            print("resume item exit")
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
            'provice',
            'city',
            'distinct',
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
