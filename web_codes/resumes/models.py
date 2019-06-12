# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from .choices import (BIRTH_YEAR_CHOICES, MAJOR_CHOICES, MARRIAGE_CHOICES, EDUCATION_TYPE_CHOICES)
from ordov.choices import (DEGREE_CHOICES, DEGREE_CHOICES_MAP)
from candidates.models import Candidate
from model_utils import Choices
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from companies.models import Post

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
    expected_industry = models.CharField(max_length=50, null=True, blank=True)
    expected_salary = models.CharField(max_length=50, null=True, blank=True)
    expected_post = models.CharField(max_length=50, null=True, blank=True)
    expected_positon = models.CharField(max_length=50, null=True, blank=True)

    expected_province = models.CharField(max_length=50, null=True, blank=True)
    expected_city = models.CharField(max_length=50, null=True, blank=True)
    expected_district = models.CharField(max_length=50, null=True, blank=True)
    expected_street = models.CharField(max_length=50, null=True, blank=True)

    # education related
    degree = models.IntegerField(blank=True, null=True, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=30, blank=True, null=True)
    school = models.CharField(max_length=30, blank=True, null=True)
    graduate_time = models.CharField(max_length=30, blank=True, null=True)
    graduate_year = models.IntegerField(null=True, blank=True)

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

    age_min = kwargs.get('age_id_min', [''])[0] or 0
    age_max = kwargs.get('age_id_max', [''])[0] or 1000

    degree_min = kwargs.get('degree_id_min', [''])[0]
    degree_max = kwargs.get('degree_id_max', [''])[0]

    graduate_time_min = kwargs.get('graduate_time_min', [''])[0]
    graduate_time_max = kwargs.get('graduate_time_max', [''])[0]

    expected_province = kwargs.get('province', [''])[0]
    expected_city = kwargs.get('city', [''])[0]
    expected_district = kwargs.get('district', [''])[0]
    #print("expected: ", expected_province, expected_city, expected_district)

    status_id = int(kwargs.get('status_id', [0])[0])

    gender_f = kwargs.get('gender_id', [''])[0]

    post_id = int(kwargs.get('post_id', [0])[0])

    if status_id == 0:
        queryset = Resume.objects.exclude(interview__post__id=post_id)
    elif status_id > 0:
        queryset = Resume.objects.filter(interview__status=status_id, interview__post__id=post_id, interview__is_active=True)
        queryset = queryset.exclude(interview__status=0, interview__post__id=post_id)
    elif status_id < 0:
        queryset = Resume.objects.filter(interview__status__gte=0, interview__post__id=post_id, interview__is_active=False)
    else:
        queryset = Resume.objects.all()

    # step1: Filter from post request
    post_request = None
    try:
        post_request = Post.objects.get(id=post_id)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        pass

    if post_request:
        post_age_min = post_request.age_min or 0
        post_age_max = post_request.age_max or 100
        post_degree_min = post_request.degree_min or 0
        post_degree_max = post_request.degree_max or 100
        post_gender = post_request.gender or ""
        post_province = post_request.address_provice
        post_city = post_request.address_city
        post_district = post_request.address_distinct

        queryset = queryset.filter(models.Q(degree__gte=post_degree_min) &
                                   models.Q(degree__lte=post_degree_max) &
                                   models.Q(age__gte=post_age_min) &
                                   models.Q(age__lte=post_age_max))
        if post_gender.find(u'男') >= 0:
            queryset = queryset.filter(models.Q(gender__contains='m'))
        elif post_gender.find(u'女') >= 0:
            queryset = queryset.filter(models.Q(gender__contains='f'))

        # post_province/city/district filter
        if post_province and post_province != "":
            queryset = queryset.filter(models.Q(expected_province__icontains=post_province))
        if post_city and post_city != "":
            queryset = queryset.filter(models.Q(expected_city__icontains=post_city))
        if post_district and post_district != "":
            queryset = queryset.filter(models.Q(expected_district__icontains=post_district))


    # step2: Filter from user-defined
    total = queryset.count()

    # filter and orderby
    if not gender_f.find(u'不限') >= 0:
        if gender_f.find(u'男') >= 0:
            queryset = queryset.filter(models.Q(gender__contains='m'))
        elif gender_f.find(u'女') >= 0:
            queryset = queryset.filter(models.Q(gender__contains='f'))

    degree_id_min = DEGREE_CHOICES_MAP.get(degree_min, 0)
    degree_id_max = 100

    age_id_min = 0
    if not age_min == '':
        age_id_min = int(age_min)
    age_id_max = 0
    if not age_max == '':
        age_id_max = int(age_max)

    if not degree_max.find(u'不限') >= 0:
        degree_id_max = DEGREE_CHOICES_MAP.get(degree_max, 100)

    queryset = queryset.filter(models.Q(degree__gte=degree_id_min) &
                               models.Q(degree__lte=degree_id_max) &
                               models.Q(age__gte=age_id_min) &
                               models.Q(age__lte=age_id_max))
    # graducate_time filter
    graduate_time_min_int = 0
    graduate_time_max_int = 100000
    if not graduate_time_min == "" and graduate_time_min.find(u'不限') < 0:
        graduate_time_min_int = int(graduate_time_min)
        queryset = queryset.filter(models.Q(graduate_year__gte=graduate_time_min_int))
    if not graduate_time_max == "" and graduate_time_max.find(u'不限') < 0:
        graduate_time_max_int = int(graduate_time_max)
        queryset = queryset.filter(models.Q(graduate_year__gte=graduate_time_max_int))

    # expected_province/city/district filter
    if not expected_province == "":
        queryset = queryset.filter(models.Q(expected_province__icontains=expected_province))
    if not expected_city == "":
        queryset = queryset.filter(models.Q(expected_city__icontains=expected_city))
    if not expected_district == "":
        queryset = queryset.filter(models.Q(expected_district__icontains=expected_district))

    # search_value box
    if search_value:
        # split the fields by blank
        # max 4 field to check
        fields = search_value.split()
        for i in range(0, min(len(fields), 4)):
            field = fields[i]
            queryset = queryset.filter(models.Q(username__icontains=field) |
                                   models.Q(phone_number__icontains=field) |
                                   models.Q(email__icontains=field) |
                                   models.Q(school__icontains=field) |
                                   models.Q(major__icontains=field) |
                                   models.Q(experience__post_name__icontains=field) |
                                   models.Q(experience__company_name__icontains=field))

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
