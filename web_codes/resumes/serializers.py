from rest_framework import serializers

from candidates.serializers import CandidateSerializer
from .models import Resume, Education

class ResumeSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(required=False)
    stat = serializers.SerializerMethodField()
    candidate_id = serializers.SerializerMethodField()

    def get_stat(self, resume):
        rt = resume.experience_set.first()
        if rt:
            print(rt.company_name)
            return str(rt.company_name)
        else:
            return None

    def get_candidate_id(self, resume):
        print(resume.candidate)
        if resume.candidate:
            print(resume.candidate.id)
            return resume.candidate.id
        else:
            return None

    class Meta:
        model = Resume
        fields = (
            'candidate_id',
            'candidate',
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
            'stat'
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

        candidate_data = validated_data.pop('candidate')
        resume = Resume.objects.create(**validated_data)
        print(resume)
        return resume

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            'resume',
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
