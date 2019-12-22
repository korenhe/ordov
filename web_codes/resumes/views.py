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
from .models import Education
from experiences.models import Experience, Project, Language, Certification
from .serializers import ResumeSerializer, EducationSerializer
from datatableview.views import DatatableView
from datatableview.utils import *
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import permissions

from accounts.models import UserProfile
from django.contrib.auth.models import User
from permissions.models import ProjectPermission

import json
import re

class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user.username, request.user.password)
        if request.user.is_authenticated is not True:
            return False
        userProfile = UserProfile.objects.get(user=request.user)
        if userProfile.user_type == "Manager":
            return True;
        elif userProfile.user_type == "Recruiter" or userProfile.user_type == "Candidate" or userProfile.user_type == "Employer":
            # To get the resumes
            # To Watching the resumes, For a Recruiter, you have limited permissions only by
            # the <post_id, stage info>
            # For Recruiter, There should never get the
            post_id = int(request.query_params.get('post_id', -999))
            if post_id == -999:
                return False
            post = None
            try:
                post = Post.objects.get(id=post_id)
            except:
                print("Could Not Found The post_id:", post_id)
                return False

            status_id = int(request.query_params.get('status_id', -999))
            if status_id == -999:
                return False
            permission = ProjectPermission.objects.filter(user=userProfile, post=post, stage=status_id)
            print("permission", permission, userProfile, post, status_id)
            if permission:
                return True
            else:
                return False
        else:
            return False
        return False

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
    permission_classes = (IsCreationOrIsAuthenticated, )

    def list(self, request, **kwargs):

        resume = query_resumes_by_args(request.user, **request.query_params)

        print("-------------------------------> add new", request.user)
        post_id = int(request.query_params.get('post_id', 0))

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
        userProfile = UserProfile.objects.get(user=self.request.user)
        if (userProfile.user_type == "Manager"):
            context['UserType'] = 'Manager'
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

# In detail View part, there are three part the
class ResumeDetail(generic.DetailView):
    model = Resume
    context_object_name = 't_resume_detail'
    template_name = 'recruit_manager/edit_resume.html'

@ensure_csrf_cookie
def ResumeDetailInfo(request, *args, **kwargs):
    idd = kwargs.get('pk', -1)
    if idd > 0:
        resume = None
        experience = None
        education = None
        project = None
        language = None
        certification = None
        try:
            resume = Resume.objects.get(pk=idd)
            experience = Experience.objects.all().filter(resume_id=idd)
            education = Education.objects.all().filter(resume_id=idd)
            project = Project.objects.all().filter(resume_id=idd)
            language = Language.objects.all().filter(resume_id=idd)
            certification = Certification.objects.all().filter(resume_id=idd)
        except ObjectDoesNotExist:
            print("Error", resume, experience, education)

        path = request.path
        isEdit = False
        if re.match(r'.*resumes/[0-9]*/edit', path):
            isEdit = True
            return render(request, "recruit_manager/edit_resume.html", locals())
        return render(request, "recruit_manager/detail_resume.html", locals())

    else:
        return HttpResponse("bad request")

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

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def get_queryset(self):
        qset = Education.objects.all()
        resume_id = self.request.query_params.get('resume_id', None)
        if resume_id is not None and resume_id.isdigit():
            qset = qset.filter(resume_id=resume_id)
        return qset
