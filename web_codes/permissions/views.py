# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from .models import ProjectPermission
from .serializers import ProjectPermissionSerializer

from django.shortcuts import render

# Create your views here.

class ProjectPermissionViewSet(viewsets.ModelViewSet):
    queryset = ProjectPermission.objects.all()
    serializer_class = ProjectPermissionSerializer

    def get_queryset(self):
        # Refer to: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
        qset = ProjectPermission.objects.all()
        post_id = self.request.query_params.get('post_id', None)
        print("get permission(", post_id, ")")
        if post_id is None or not post_id.isdigit():
            return qset
        qset = qset.filter(post_id=post_id)
        return qset
