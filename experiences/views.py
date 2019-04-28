# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

from .models import Experience
from .serializers import ExperienceSerializer

class ExperienceView(APIView):
    def get(self, request):
        experiences = Experience.objects.all()

        serializer = ExperienceSerializer(experiences, many=True)
        return Response ({"experiences": serializer.data})

    def post(self, request):
        print(request.POST)
        experience = request.data.get('experience')

        serializer = ExperienceSerializer(data=experience)
        if serializer.is_valid(raise_exception=True):
            experience_saved = serializer.save()

        return Response(
            {"success": "Experience '{}' created successfully".format(experience_saved.company_name)}
        )
