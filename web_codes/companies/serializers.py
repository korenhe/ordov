from rest_framework import serializers

from .models import Company, Department, Post

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

    def create(self, validated_data):
        company_data = validated_data.pop('company')

        company = CompanySerializer.create(CompanySerializer(), validated_data=company_data)

        department, created = Department.objects.update_or_create(
            company=company,
            **validated_data)

        return department

class PostSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(required=True)

    class Meta:
        model = Post
        fields = (
            'department',

            'name',
            'description',
            'level',
        )

    def create(self, validated_data):
        department_data = validated_data.pop('department')

        department_ = DepartmentSerializer.create(DepartmentSerializer(), validated_data=department_data)
        company_ = department_.company

        post, created = Post.objects.update_or_create(
            company=company_,
            department=department_,
            **validated_data)

        return post
