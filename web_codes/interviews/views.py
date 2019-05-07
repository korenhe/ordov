# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from rest_framework.views import APIView
from rest_framework import viewsets

from .models import Interview
from .serializers import InterviewSerializer

# Create your views here.
class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all().order_by('id')
    serializer_class = InterviewSerializer

class InterviewTable(generic.ListView):
    context_object_name = 't_interview_list'
    template_name = 'interviews/table_interviews.html'

    def get_queryset(self):
        return Interview.objects.all()

    def get_context_data(self, **kwargs):
        context = super(InterviewTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Interview'
        return context
