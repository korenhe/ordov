# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from .choices import (DEGREE_CHOICES, BIRTH_YEAR_CHOICES, MAJOR_CHOICES, MARRIAGE_CHOICES, EDUCATION_TYPE_CHOICES)
from candidates.models import Candidate

# Create your models here.

class Resume(models.Model):
    # The Resume would be linked to a candidate afterwards
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, blank=True, null=True)
    resume_id = models.IntegerField(null=True)
    visible = models.BooleanField(default=False)
    resume_way = models.CharField(max_length=20, blank=True, null=True)
    resume_way2 = models.CharField(max_length=20, blank=True, null=True)

    # base info
    username = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(choices=(("m", "男"), ("f", "女"),), max_length=1, blank=True, null=True)
    birth_year = models.CharField(max_length=4, blank=True, null=True, choices=BIRTH_YEAR_CHOICES)
    birth_month = models.CharField(max_length=4, blank=True, null=True)
    birth_day = models.CharField(max_length=4, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    identity = models.CharField(max_length=25, blank=True, null=True)
    age = models.IntegerField(null=True)

    # birth place (jiguan in chinese)
    birth_provice = models.CharField(max_length=10, blank=True, null=True)
    birth_city = models.CharField(max_length=10, blank=True, null=True)
    birth_distinct = models.CharField(max_length=10, blank=True, null=True)
    birth_place = models.CharField(max_length=50, blank=True, null=True)

    # social info
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    qq = models.BigIntegerField(null=True, blank=True)
    residence = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    marriage = models.CharField(max_length=10, blank=True, null=True, choices=MARRIAGE_CHOICES)
    live_state = models.CharField(max_length=10, blank=True, null=True)

    # resident info
    current_settle_provice = models.CharField(max_length=10, blank=True, null=True)
    current_settle_city = models.CharField(max_length=10, blank=True, null=True)
    current_settle_distinct = models.CharField(max_length=10, blank=True, null=True)
    current_settle_street = models.CharField(max_length=20, blank=True, null=True)
    birth_place = models.CharField(max_length=50, blank=True, null=True)

    # Expection info
    expected_area = models.CharField(max_length=50, null=True, blank=True)
    expected_salary = models.CharField(max_length=50, null=True, blank=True)
    expected_post = models.CharField(max_length=50, null=True, blank=True)
    expected_positon = models.CharField(max_length=50, null=True, blank=True)

    # education related
    degree = models.IntegerField(blank=True, null=True, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=30, blank=True, null=True)
    school = models.CharField(max_length=30, blank=True, null=True)
    graduate_time = models.CharField(max_length=30, blank=True, null=True)

    # Text Fieled
    self_description = models.TextField(max_length=500, blank=True, null=True, default='')

    # reserved Field
    reserved1 = models.CharField(max_length=50, blank=True, null=True, default='')
    reserved2 = models.CharField(max_length=50, blank=True, null=True, default='')

    # table related info
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__ (self):
        return self.username

def query_resumes_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    age_min = kwargs.get('age_min', None)[0] or 0
    age_max = kwargs.get('age_max', None)[0] or 100

    degree_min = kwargs.get('degree_min', None)[0] or 0
    degree_max = kwargs.get('degree_max', None)[0] or 10

    gender_f = kwargs.get('gender_f', None) or False
    gender_m = kwargs.get('gender_m', None) or False

    queryset = Resume.objects.all()
    total = queryset.count()

    # filter and orderby
    queryset = queryset.filter(models.Q(age__range=[age_min, age_max]) &
                               models.Q(degree__range=[degree_min, degree_max]))

    if not gender_f:
        queryset = queryset.filter(models.Q(gender__contains='m'))
    elif not gender_m:
        queryset = queryset.filter(models.Q(gender__contains='f'))

    count = queryset.count()

    queryset = queryset[start:start + length]
    # final decoration
    for q in queryset:
        q.degree = DEGREE_CHOICES[q.degree][1]
        q.gender = "Female" if (q.gender == 'f') else "Male"

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw' : draw,
    }

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, default='')
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    # basic info
    school = models.CharField(max_length=50, blank=True, null=True)
    college = models.CharField(max_length=50, blank=True, null=True)
    major = models.CharField(max_length=50, blank=True, null=True)
    degree = models.IntegerField(choices=DEGREE_CHOICES, blank=True, null=True)
    edu_type = models.CharField(max_length=50, choices=EDUCATION_TYPE_CHOICES, blank=True, null=True)

    # resident info
    provice = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=10, blank=True, null=True)
    distinct = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=20, blank=True, null=True)
    place = models.CharField(max_length=50, blank=True, null=True)

    instructor = models.CharField(max_length=50, blank=True, null=True)
    instructor_phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.degree
