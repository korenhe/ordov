# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

from .models import Interview, query_interviews_by_args
from .serializers import InterviewSerializer
from companies.models import Post
from resumes.models import Resume

# Create your views here.
class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all().order_by('id')
    serializer_class = InterviewSerializer

    def list(self, request, **kwargs):

        interview = query_interviews_by_args(**request.query_params)

        serializer = InterviewSerializer(interview['items'], many=True)
        result = dict()

        result['data'] = serializer.data
        tds = result['data']

        print(result)
        # here we can modify the response data, and we can add pesudo fields in
        # serializer, as we handled candidate_id
        for td in tds:
            resume = Resume.objects.get(pk=td['resume']).username
            post = Post.objects.get(pk=td['post']).name
            td.update({'resume': resume})
            td.update({'post': post})
#            td.update({'DT_RowId': td['resume']})

        result['draw'] = interview['draw']
        result['recordsTotal'] = int(interview['total'])
        result['recordsFiltered'] = int(interview['count'])

        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

class InterviewTable(generic.ListView):
    context_object_name = 't_interview_list'
    template_name = 'interviews/table_interviews.html'

    def get_queryset(self):
        return Interview.objects.all()

    def get_context_data(self, **kwargs):
        context = super(InterviewTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Interview'
        return context
