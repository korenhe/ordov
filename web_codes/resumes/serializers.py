from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from candidates.models import Candidate
from .models import Resume

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = (
            'user',
        )

class ResumeSerializer(serializers.ModelSerializer):
    #phone_number = PhoneNumberField(required=True)
    candidate = CandidateSerializer(required=True)

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
        candidate_data = validated_data.pop('candidate')
        candidate = CandidateSerializer.create(CandidateSerializer(), validated_data=candidate_data)

        resume, created = Resume.objects.update_or_create(
            candidate=candidate, **validated_data)

        return resume
