# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

# Create your views here.
from .models import Resume
from .serializers import ResumeSerializer, EducationSerializer

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

def query_resumes_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    print(start, length)
    queryset = Resume.objects.all()
    total = queryset.count()
    count = queryset.count()

    queryset = queryset[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw' : draw,
    }

class ResumeViewSet(viewsets.ModelViewSet):
    print("==================")
    queryset = Resume.objects.all().order_by('id')
    serializer_class = ResumeSerializer

    def list(self, request, **kwargs):

        resume = query_resumes_by_args(**request.query_params)
        serializer = ResumeSerializer(resume['items'], many=True)
        result = dict()

        result['data'] = serializer.data
        result['draw'] = resume['draw']
        print(resume['total'], resume['count'])
        result['recordsTotal'] = int(resume['total'])
        result['recordsFiltered'] = int(resume['count'])

        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
#        return Response(serializer.data)

class ResumeTable(generic.ListView):
    context_object_name = 't_resume_list'
    template_name = 'resumes/table_resumes.html'

    def get_queryset(self):
        return Resume.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ResumeTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Resume'

        return context

class ResumeDetail(generic.DetailView):
    model = Resume
    context_object_name = 't_resume_detail'
    template_name = 'recruit_manager/detail_resume.html'

class EducationView(APIView):
    def get(self, request):
        education = Education.objects.all()
        serializer = EducationSerializer(education, many=True)
        return Response({"educations": serializer.data})
    def post(self, request):
        education = request.data.get('education')
        serializer = EducationSerializer(data=education)
        if serializer.is_valid(raise_exception=True):
            education_saved = serializer.save()
        return Response(
            {"success": "Education '{}' created successfully".format(education_saved.school)}
        )
