from rest_framework import serializers

from .models import Area, Company, Department, Post

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'name',
            'description',
            )
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'name',
            'short_name',
            'description',
            'scale',

            'area',
            'c_type',
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
    id = serializers.SerializerMethodField()

    def get_id(self, post):
        return post.id

    class Meta:
        model = Post
        fields = (
            'id',
            'department',

            'name',
            'description',
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
