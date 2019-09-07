# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

# Create your views here.

from .models import Experience, Project, Language, Certification
from .serializers import ExperienceSerializer, ProjectSerializer, LanguageSerializer, CertificationSerializer

class ExperienceView(APIView):
    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response ({"experiences": serializer.data})

    def post(self, request):
        experience = request.data.get('experience')

        serializer = ExperienceSerializer(data=experience)
        if serializer.is_valid(raise_exception=True):
            experience_saved = serializer.save()

        return Response(
            {"success": "Experience '{}' created successfully".format(experience_saved.company_name)}
        )

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        # Refer to: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
        queryset = Experience.objects.all()
        resume_id = self.request.query_params.get('resume_id', None)
        if resume_id is not None:
            queryset = queryset.filter(resume_id=resume_id)
        return queryset

class ProjectView(APIView):
    def get(self, request):
        project = Project.objects.all()

        serializer = ProjectSerializer(project, many=True)
        return Response ({"project": serializer.data})

    def post(self, request):
        project = request.data.get('project')

        serializer = ProjectSerializer(data=project)
        if serializer.is_valid(raise_exception=True):
            project_saved = serializer.save()

        return Response(
            {"success": "Project '{}' created successfully".format(project_saved.brief)}
        )

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        resume_id = self.request.query_params.get('resume_id', None)
        if resume_id is not None:
            queryset = queryset.filter(resume_id=resume_id)
        return queryset

class LanguageView(APIView):
    def get(self, request):
        language = Language.objects.all()

        serializer = LanguageSerializer(language, many=True)
        return Response ({"language": serializer.data})

    def post(self, request):
        language = request.data.get('language')

        serializer = LanguageSerializer(data=language)
        if serializer.is_valid(raise_exception=True):
            language_saved = serializer.save()

        return Response(
            {"success": "Language '{}' created successfully".format(language_saved.name)}
        )

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def get_queryset(self):
        queryset = Language.objects.all()
        resume_id = self.request.query_params.get('resume_id', None)
        if resume_id is not None:
            queryset = queryset.filter(resume_id=resume_id)
        return queryset


class CertificationView(APIView):
    def get(self, request):
        certification = Certification.objects.all()

        serializer = CertificationSerializer(certification, many=True)
        return Response ({"certification": serializer.data})

    def post(self, request):
        certification = request.data.get('certification')

        serializer = CertificationSerializer(data=certification)
        if serializer.is_valid(raise_exception=True):
            certification_saved = serializer.save()

        return Response(
            {"success": "Certification '{}' created successfully".format(certification_saved.name)}
        )
