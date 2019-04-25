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

    company = CompanySerializer(required=True)

    class Meta:
        model = Department
        fields = (
            'company', # foreignkey

            'name',
            'description',
        )

        depth = 1

    def create(self, validated_data):
        company_data = validated_data.pop('company')

        company = CompanySerializer.create(CompanySerializer(), validated_data=company_data)

        department, created = Department.objects.update_or_create(
            company=company,
            **validated_data)

        return department
