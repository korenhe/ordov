# -*- coding: utf-8 -*- from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

# Create your views here.

from .models import Company, Department, Post, query_posts_by_args
from .serializers import CompanySerializer, DepartmentSerializer, PostSerializer

from ordov.choices import (DEGREE_CHOICES, DEGREE_CHOICES_MAP)

from django.http import HttpResponse, HttpResponseRedirect

from rest_framework import permissions
from accounts.models import UserProfile
from django.contrib.auth.models import User
from permissions.models import ProjectPermission

class CompanyView(APIView):
    def get(self, request):
        companies = Company.objects.all()

        serializer = CompanySerializer(companies, many=True)
        return Response ({"companies": serializer.data})

    def post(self, request):
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
        department = request.data.get('department')

        serializer = DepartmentSerializer(data=department)
        if serializer.is_valid(raise_exception=True):
            department_saved = serializer.save()

        return Response(
            {"success": "Department '{}' created successfully".format(department_saved.name)}
        )

class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response ({"posts": serializer.data})

    def post(self, request):
        post = request.data.get('post')

        serializer = PostSerializer(data=post)
        if serializer.is_valid(raise_exception=True):
            post_saved = serializer.save()

        return Response(
            {"success": "Post '{}' created successfully".format(post_saved.name)}
        )

class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user.username, request.user.password)
        if request.user.is_authenticated is not True:
            print("user.is_authenticated", request.user.is_authenticated)
            return False
        userProfile = UserProfile.objects.get(user=request.user)
        if userProfile.user_type == "Manager":
            return True;
        elif userProfile.user_type == "Recruiter" or userProfile.user_type == "Candidate" or userProfile.user_type == "Employer":
            post_id = int(request.query_params.get('post_id', -999))
            if post_id == -999:
                return False
            status_id = int(request.query_params.get('status_id', -999))
            if status_id == -999:
                return False
            try:
                permission = ProjectPermission.objects.get(post=post_id, stage=status_id, user=userProfile)
                print("Found Permission", permission.id)
                return True
            except:
                return False
        else:
            print("Fail")
            return False
        return False

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    permission_classes = (IsCreationOrIsAuthenticated, )

    def list(self, request, **kwargs):

        post = query_posts_by_args(**request.query_params)

        serializer = PostSerializer(post['items'], many=True)
        result = dict()

        result['data'] = serializer.data
        tds = result['data']

        for td in tds:
            td.update({'DT_RowId': td['id']})

        result['draw'] = post['draw']
        result['recordsTotal'] = int(post['total'])
        result['recordsFiltered'] = int(post['count'])

        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

class PostTable(generic.ListView):
    context_object_name = 't_post_list'
    template_name = 'companies/table_posts.html'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Post'
        return context

# TODO: This is a temporary method for update resume from ajax
# and would be removed afterwards
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def UpdatePost(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        department_name = request.POST['department_name']
        post_name = request.POST['post_name']
        baiying_task = request.POST['baiying_task_id']
        p_type = request.POST['post_type']

        province = request.POST['working_place_province']
        city = request.POST['working_place_city']
        district = request.POST['working_place_district']

        if company_name == "" or department_name == "" or post_name == "" or p_type == "":
            return HttpResponse("fail")

        if province == "" and city == "" and district == "":
            return HttpResponse("fail")

        baiying_fields = baiying_task.split('-')
        if len(baiying_fields) < 2:
            return HttpResponse("fail")
        baiying_task_name = baiying_fields[0]
        baiying_task_id = baiying_fields[1]

        min_degree = request.POST['degree_id_min']
        max_degree = request.POST['degree_id_max']
        min_age = request.POST['age_id_min']
        max_age = request.POST['age_id_max']
        graduate_start = request.POST['graduate_time_start']
        graduate_end = request.POST['graduate_time_end']

        gender = request.POST['gender_id']
        salary = request.POST['min_salary_id']
        linkman_name = request.POST['linkman_name']
        linkman_phone = request.POST['linkman_phone']

        project_name = company_name + "-" + province + city + district + "-" + p_type
        ageMin = 0
        if not request.POST['age_id_min'] == "":
            ageMin = int(request.POST['age_id_min'])
        ageMax = 100
        if not request.POST['age_id_max'] == "":
            ageMax = int(request.POST['age_id_max'])

        degreeMin = DEGREE_CHOICES_MAP.get(min_degree, 0)
        degreeMax = 100
        if not max_degree.find(u'不限') >= 0:
            degreeMax= DEGREE_CHOICES_MAP.get(max_degree, 100)

        graduate_S = 0
        if not graduate_start == "" and graduate_start.find(u'不限') < 0:
            graduate_S = int(graduate_start)
        graduate_E = 2080
        if not graduate_end == "" and graduate_end.find(u'不限') < 0:
            graduate_E = int(graduate_end)

        salary_offer = request.POST['min_salary_id']

        resume_latest_modified = request.POST['resume_latest_modified']

        post_info = {
            "department": {
                "description": "",
                "company": {
                    "c_type":"",
                    "name": company_name,
                    "scale": 0,
                    "area": "",
                    "description": "",
                    "short_name": company_name
                },
                "name": department_name
            },
            "description": post_name,
            "name": post_name,
            "address_province": province,
            "address_city": city,
            "address_district": district,
            "salary_offer": salary_offer
        }
        """
        Do Not Use the serializer here
        """
        companyTarget = None
        departTarget = None
        postTarget = None
        company_info = {
            "c_type":"",
            "name": company_name,
            "scale": 0,
            "area": "",
            "description": "",
            "short_name": company_name
        }
        department_info = {
            "description": "",
            "name": department_name
        }
        post_info = {
            "description": post_name,
            "name": post_name,
            "degree": DEGREE_CHOICES_MAP.get(min_degree),
            "degree_min": degreeMin,
            "degree_max": degreeMax,
            "address_province": province,
            "address_city": city,
            "address_district": district,
            "age_min": ageMin,
            "age_max": ageMax,
            "graduatetime_min": graduate_S,
            "graduatetime_max": graduate_E,
            "salary_offer": salary_offer,
            "gender": gender,
            "linkman": linkman_name,
            "linkman_phone": linkman_phone,
            "project_name": project_name,
            "p_type": p_type,
            "baiying_task_name": baiying_task_name,
            "baiying_task_id": int(baiying_task_id),
            "resume_latest_modified": resume_latest_modified,
            "level": ""
        }

        companyTarget, created = Company.objects.update_or_create(**company_info)
        departmentTarget, created = Department.objects.update_or_create(company=companyTarget, **department_info)
        postTarget, created = Post.objects.update_or_create(company=companyTarget, department=departmentTarget, **post_info)

        # After the post info created, we should add the
        # the right to the owner, and by the
        return HttpResponse("success")

        """
        serializer = PostSerializer(data=post_info)
        if serializer.is_valid(raise_exception=True):
            post_saved = serializer.save()
        else:
            print("Fail to serialize the post")
        """
    return HttpResponse("fail")
