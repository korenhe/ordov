# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

from .models import Company, Department
from .serializers import CompanySerializer, DepartmentSerializer

class CompanyView(APIView):
    def get(self, request):
        companies = Company.objects.all()

        serializer = CompanySerializer(companies, many=True)
        return Response ({"companies": serializer.data})

    def post(self, request):
        print(request.POST)
        company = request.data.get('company')

        serializer = CompanySerializer(data=company)
        if serializer.is_valid(raise_exception=True):
            company_saved = serializer.save()

        return Response(
            {"success": "Company '{}' created successfully".format(company_saved.name)}
        )

class DepartmentView(APIView):
    def get(self, request):
        departments = Department.objects.all()

        serializer = DepartmentSerializer(departments, many=True)
        return Response ({"departments": serializer.data})

    def post(self, request):
        print(request.POST)
        department = request.data.get('department')

        serializer = DepartmentSerializer(data=department)
        if serializer.is_valid(raise_exception=True):
            department_saved = serializer.save()

        return Response(
            {"success": "Department '{}' created successfully".format(department_saved.name)}
        )

