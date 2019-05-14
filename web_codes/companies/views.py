# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

# Create your views here.

from .models import Company, Department, Post, query_posts_by_args
from .serializers import CompanySerializer, DepartmentSerializer, PostSerializer

class CompanyView(APIView):
    def get(self, request):
        companies = Company.objects.all()

        serializer = CompanySerializer(companies, many=True)
        return Response ({"companies": serializer.data})

    def post(self, request):
        print(request.POST)
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
        print(request.POST)
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
        print(request.POST)
        post = request.data.get('post')

        serializer = PostSerializer(data=post)
        if serializer.is_valid(raise_exception=True):
            post_saved = serializer.save()

        return Response(
            {"success": "Post '{}' created successfully".format(post_saved.name)}
        )

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer

    def list(self, request, **kwargs):

        post = query_posts_by_args(**request.query_params)

        serializer = PostSerializer(post['items'], many=True)
        result = dict()

        result['data'] = serializer.data
        tds = result['data']

        for td in tds:
            print(td)
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
