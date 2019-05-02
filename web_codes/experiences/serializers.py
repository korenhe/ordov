from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            'resume',
            'start',
            'end',

            'company_name',
            'department_name',
            'post_name',

            'work_province',
            'work_city',
            'work_district',

            'level',
            'description',
            'salary',
            'leave_reason',
            'shift',

            'witness',
            'witness_phone'
            )
