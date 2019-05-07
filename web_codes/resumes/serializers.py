from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from candidates.serializers import CandidateSerializer
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    #phone_number = PhoneNumberField(required=True)
    candidate = CandidateSerializer(required=False)
    stat = serializers.SerializerMethodField('is_named_bar')

    def is_named_bar(self, resume):
        print("here")
        rt = resume.experience_set.first()
        if rt:
            print(rt.company_name)
            return str(rt.company_name)
        else:
            return None

    class Meta:
        model = Resume
        fields = (
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
        try:
            candidate_data = validated_data.pop('candidate')
            candidate = CandidateSerializer.create(CandidateSerializer(), validated_data=candidate_data)

            resume, created = Resume.objects.update_or_create(
                candidate=candidate, **validated_data)
            return resume
        except KeyError:

            resume = Resume.objects.create(**validated_data)
            return resume
