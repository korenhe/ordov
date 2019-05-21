# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

# Create your views here.
from .models import Resume, query_resumes_by_args
from companies.models import Post
from .serializers import ResumeSerializer, EducationSerializer
from datatableview.views import DatatableView
from datatableview.utils import *

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

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all().order_by('id')
    serializer_class = ResumeSerializer

    def list(self, request, **kwargs):

        resume = query_resumes_by_args(**request.query_params)

        post_id = int(request.query_params.get('post_id', None)[0])

        serializer = ResumeSerializer(
            resume['items'],
            many=True,
            context={'post_id': post_id}
        )
        result = dict()

        result['data'] = serializer.data
        tds = result['data']

        # here we can modify the response data, and we can add pesudo fields in
        # serializer, as we handled candidate_id
        for td in tds:
            td.update({'DT_RowId': td['id']})

        result['draw'] = resume['draw']
        result['recordsTotal'] = int(resume['total'])
        result['recordsFiltered'] = int(resume['count'])

        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

class ResumeTable(generic.ListView):
    context_object_name = 't_resume_list'
    template_name = 'resumes/table_resumes.html'

    def get_queryset(self):
        return Resume.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ResumeTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Resume'

        return context

class MultiTable(generic.ListView):
    context_object_name = 't_resume_list'
    template_name = 'resumes/table_multi.html'

    def get_queryset(self):
        return Resume.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MultiTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Resume'

        return context


class CompositeTable(DatatableView):
    model = Resume

    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns' : [
            ('Resume', 'resume_id'),
            ('Name', 'username'),
            ('Gender', 'gender'),
            ('Age', 'age'),
            ('Phone', 'phone_number'),
            ('Email', 'email'),
            ('School', 'school'),
            ('Degree', 'degree'),
            ('Major', 'major'),
            ('Stat', None, 'get_entry_stat')
        ]}

    def get_entry_stat(self, instance, *args, **kwargs):
        return "ABC{}".format(instance.username)

    post_datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            'company',
            'department',
            'name',
        ]
    }

    def get_queryset(self, type=None):
        """
        Customized implementation of the queryset getter.  The custom argument ``type`` is managed
        by us, and is used in the context and GET parameters to control which table we return.
        """
        if type is None:
            type = self.request.GET.get('datatable-type', None)

        if type == "C_POST":
            return Post.objects.all()
        return super(CompositeTable, self).get_queryset()

    def get_datatable_options(self, type=None):
        """
        Customized implementation of the options getter.  The custom argument ``type`` is managed
        by us, and is used in the context and GET parameters to control which table we return.
        """
        if type is None:
            type = self.request.GET.get('datatable-type', None)

        options = self.datatable_options

        if type == "C_POST":
            # Return separate options settings
            options = self.post_datatable_options

        return options

    def get_datatable(self, type=None):
        """
        Customized implementation of the structure getter.  The custom argument ``type`` is managed
        by us, and is used in the context and GET parameters to control which table we return.
        """
        if type is None:
            type = self.request.GET.get('datatable-type', None)

        if type is not None:
            datatable_options = self.get_datatable_options(type=type)
            # Put a marker variable in the AJAX GET request so that the table identity is known
            ajax_url = self.request.path + "?datatable-type={type}".format(type=type)

        if type == "C_POST":
            # Change the reference model to Blog, instead of Entry
            datatable = get_datatable_structure(ajax_url, datatable_options, model=Post)
        else:
            return super(CompositeTable, self).get_datatable()

        return datatable


    def get_context_data(self, **kwargs):
        context = super(CompositeTable, self).get_context_data(**kwargs)

        # Get the other structure objects for the initial context
        context['post_datatable'] = self.get_datatable(type="C_POST")

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
