from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    #phone_number = PhoneNumberField(required=True)

    class Meta:
        model = Candidate
        fields = (
            'name',
            'gender',
            'birth_year',
            'birth_month',
            'date_of_birth',
            'identity',

            'phone_number',
            'qq',
            'residence',
            'email',
            'marriaged',

            'degree',
            'major',
            'school',

        )
