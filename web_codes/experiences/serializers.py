from rest_framework import serializers

from .models import Experience, Project, Language, Certification
from resumes.models import Resume
from resumes.serializers import ResumeSerializer

class ExperienceSerializer(serializers.ModelSerializer):
    # DON'T WRAP EMBEDDED FOREIGN KEY OBJECT HERE.
    # TBD: PostSerializer
    class Meta:
        model = Experience
        fields = (
            'id',
            'resume', # foreign key
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
            'duty',
            'description',

            'witness',
            'witness_phone'
        )

class ProjectSerializer(serializers.ModelSerializer):
    # DON'T WRAP EMBEDDED FOREIGN KEY OBJECT HERE.
    # TBD: PostSerializer
    class Meta:
        model = Project
        fields = (
            'id',
            'resume',
            'start',
            'end',

            'name',
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
            'id',
            'resume',
            'name',
            'cert',
            "description",
        )

class CertificationSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(required=True)
    class Meta:
        model = Certification
        fields = (
            'resume',
            'time',
            'name',
            "institution",
            "description",
        )

    def create(self, validated_data):
        resume_data = validated_data.pop('resume')
        resume = ResumeSerializer.create(ResumeSerializer(), validated_data = resume_data)
        certification, created = Certification.objects.update_or_create(
            resume=resume, **validated_data)
        return certification
