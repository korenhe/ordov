from rest_framework import serializers

from .models import Experience, Project, Language, Certification

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
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'resume',
            'start',
            'end',

            "brief",
            "scale",
            "role",

            "company_name",
            "duty",
            "summary"
            )

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            'resume',
            'name',
            'cert',
            "description",
        )


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = (
            'resume',
            'time',
            'name',
            "institution",
            "description",
        )

