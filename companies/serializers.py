from rest_framework import serializers

from .models import Company, Department

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'name',
            'short_name',
            'description',
            'scale',

            'area',
            'cType',
            )

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'company', # foreignkey

            'name',
            'description',
        )

        depth = 1
