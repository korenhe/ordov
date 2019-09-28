# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from .models import ProjectPermission
from .serializers import ProjectPermissionSerializer

from rest_framework import permissions

from django.shortcuts import render

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Create your views here.

# https://stackoverflow.com/questions/30871033/django-rest-framework-remove-csrf
class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        print("------------> permission..  -------------->")
        return True

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class ProjectPermissionViewSet(viewsets.ModelViewSet):
    queryset = ProjectPermission.objects.all()
    serializer_class = ProjectPermissionSerializer
    permission_classes = (IsCreationOrIsAuthenticated, )
    #authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        # Refer to: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
        qset = ProjectPermission.objects.all()
        post_id = self.request.query_params.get('post', None)
        print("get permission(", post_id, ")")
        if post_id is None or not post_id.isdigit():
            return qset
        qset = qset.filter(post_id=post_id)
        stage_id = self.request.query_params.get('stage', None)
        print("get permission(", post_id, ") stage(", stage_id, ")")
        if stage_id is not None and stage_id.isdigit():
            qset = qset.filter(stage=stage_id)
        user_id  = self.request.query_params.get('user', None)
        if user_id is not None and user_id.isdigit():
            qset = qset.filter(user_id=user_id)

        return qset
