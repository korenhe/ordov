# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .models import Resume
from .serializers import ResumeSerializer

class ResumeView(APIView):
    def get(self, request):
        resumes = Resume.objects.all()

        # resumes, generate more than one single resume, so many=true
        serializer = ResumeSerializer(resumes, many=True)
        return Response ({"resumes": serializer.data})

    def post(self, request):
        resume = request.data.get('resume')

        serializer = ResumeSerializer(data=resume)
        if serializer.is_valid(raise_exception=True):
            resume_saved = serializer.save()

        return Response(
            {"success": "Resume '{}' created successfully".format(resume_saved.username)}
        )
