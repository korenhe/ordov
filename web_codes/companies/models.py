# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    short_name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    scale = models.IntegerField(default=0)
    # choice
    area = models.CharField(max_length=50)
    cType = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    # reserved
    reserved1 = models.CharField(max_length=50, blank=True, null=True, default='')
    reserved2 = models.CharField(max_length=50, blank=True, null=True, default='')

    def __str__(self):
        return self.name

class Post(models.Model):
    # TODO: to confirm it is safe to hierarchy CASCADE here
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    pType = models.CharField(max_length=50, blank=True, null=True, default='')
    pFeature = models.CharField(max_length=50, blank=True, null=True, default='')
    description = models.CharField(max_length=1000, blank=True, null=True, default='')
    # the level field should be in experience table
    #level = models.CharField(max_length=20, blank=True, null=True, default='')

    # reserved
    reserved1 = models.CharField(max_length=50, blank=True, null=True, default='')
    reserved2 = models.CharField(max_length=50, blank=True, null=True, default='')

    def __str__(self):
        return "%s,%s,%s" % (self.name, self.department.name, self.company.name)

def query_posts_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    queryset = Post.objects.all()
    total = queryset.count()

    # filter and orderby
    count = queryset.count()

    queryset = queryset[start:start + length]

    # final decoration

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw' : draw,
    }
