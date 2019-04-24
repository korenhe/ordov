# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .models import Candidate
from .serializers import CandidateSerializer

class CandidateView(APIView):
    def get(self, request):
        candidates = Candidate.objects.all()

        # candidates, generate more than one single candiate, so many=true
        serializer = CandidateSerializer(candidates, many=True)
        return Response ({"candidates": serializer.data})

    def post(self, request):
        print(request.POST)
        candidate = request.data.get('candidate')

        print('candidate={}'.format(candidate))
        serializer = CandidateSerializer(data=candidate)
        if serializer.is_valid(raise_exception=True):
            print("is valid in")
            candidate_saved = serializer.save()

        return Response(
            {"success": "Candidate '{}' created successfully".format(candidate_saved.name)}
        )
