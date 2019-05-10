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
