# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from .choices import (BIRTH_YEAR_CHOICES, MAJOR_CHOICES, MARRIAGE_CHOICES, EDUCATION_TYPE_CHOICES)
from ordov.choices import (DEGREE_CHOICES, DEGREE_CHOICES_MAP)
from candidates.models import Candidate
from model_utils import Choices

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

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'), #CK
    ('1', 'interview_id'), #IID
    ('2', 'candidate_id'), #CID
    ('3', 'id'), #ID
    ('4', 'username'), # *Name
    ('5', 'gender'), # Gender
    ('6', 'age'), # Age
    ('7', 'phone_number'), #Phone
    ('8', 'email'), #email
    ('9', 'school'), #school
    ('10', 'degree'), #degree
    ('11', 'major'), # *Major
    ('12', 'is_match'), # ismatch
    ('13', 'status'), # status
    ('14', 'id'), # action
)

def query_resumes_by_args(**kwargs):
    draw = int(kwargs.get('draw', [0])[0])
    length = int(kwargs.get('length', [10])[0])
    start = int(kwargs.get('start', [0])[0])
    search_value = kwargs.get('search[value]', [0])[0]
    order_column = kwargs.get('order[0][column]', [0])[0]
    order = kwargs.get('order[0][dir]', [0])[0]

    order_column = ORDER_COLUMN_CHOICES[int(order_column)][1]
    if order == 'desc':
        order_column = '-' + order_column

    age_min = kwargs.get('age_id', [0])[0] or 0

    degree_min = kwargs.get('degree_id', [0])[0] or 0

    status_id = int(kwargs.get('status_id', [0])[0])

    gender_f = kwargs.get('gender_id', [''])[0]

    post_id = int(kwargs.get('post_id', [0])[0])

    if status_id:
        if status_id >= 0:
            queryset = Resume.objects.filter(interview__status=status_id, interview__post__id=post_id)
            queryset = queryset.exclude(interview__status=0, interview__post__id=post_id)
        else:
            queryset = Resume.objects.filter(interview__status__lte = 0, interview__post__id=post_id)
    else:
        queryset = Resume.objects.all()
        queryset = queryset.exclude(interview__status=0, interview__post__id=post_id)

    total = queryset.count()

    # filter and orderby
    if not gender_f.find(u'不限') >= 0:
        if gender_f.find(u'男') >= 0:
            queryset = queryset.filter(models.Q(gender__contains='m'))
        elif gender_f.find(u'女') >= 0:
            queryset = queryset.filter(models.Q(gender__contains='f'))

    degree_id = DEGREE_CHOICES_MAP.get(degree_min, 0)

    queryset = queryset.filter(models.Q(degree__gte=degree_id) &
                               models.Q(age__gte=age_min))


    # search_value box
    if search_value:
        queryset = queryset.filter(models.Q(username__icontains=search_value) |
                                   models.Q(phone_number__icontains=search_value) |
                                   models.Q(email__icontains=search_value) |
                                   models.Q(school__icontains=search_value) |
                                   models.Q(major__icontains=search_value))

    # ------
    count = queryset.count()

    queryset = queryset.order_by(order_column)[start:start + length]

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

    # table related info
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.degree
