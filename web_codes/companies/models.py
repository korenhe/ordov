# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from model_utils import Choices
from .choices import SCALE_CHOICES
from ordov.choices import DEGREE_CHOICES

# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(blank=True, null=True, default='')

    # table related info
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

class Company(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True, default='')
    scale = models.IntegerField(default=0, blank=True, null=True)
    scale2 = models.TextField(blank=True, null=True, choices=SCALE_CHOICES)

    registerd_capital = models.IntegerField(default=0, blank=True, null=True)
    founding_time = models.DateField(blank=True, null=True)
    # unified social credit code
    uscc = models.CharField(max_length=50, blank=True, null=True)

    address_provice = models.CharField(max_length=10, blank=True, null=True)
    address_city = models.CharField(max_length=10, blank=True, null=True)
    address_distinct = models.CharField(max_length=10, blank=True, null=True)
    address_stress = models.CharField(max_length=20, blank=True, null=True)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)

    # image and radio
    business_licence = models.ImageField(blank=True, null=True);
    #introduce_radio = models.

    # choice
    area_ptr = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    c_type = models.CharField(max_length=50, blank=True, null=True)

    # table related info
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.name

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True)

    # reserved
    reserved1 = models.CharField(max_length=50, blank=True, null=True, default='')
    reserved2 = models.CharField(max_length=50, blank=True, null=True, default='')

    # table related info
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    # TODO: to confirm it is safe to hierarchy CASCADE here
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    project_name = models.CharField(max_length=50, blank=True, null=True)

    p_type = models.CharField(max_length=50, blank=True, null=True, default='')
    p_feature = models.CharField(max_length=50, blank=True, null=True, default='')
    p_xingzhi = models.CharField(max_length=50, blank=True, null=True, default='')
    description = models.CharField(max_length=1000, blank=True, null=True, default='')
    # the level field should be in experience table
    level = models.CharField(max_length=20, blank=True, null=True, default='')
    subsidy = models.CharField(max_length=20, blank=True, null=True, default='')
    sum_salaray = models.CharField(max_length=20, blank=True, null=True, default='')
    year_yard = models.CharField(max_length=20, blank=True, null=True, default='')
    social_security = models.CharField(max_length=20, blank=True, null=True, default='')
    other_benefit = models.CharField(max_length=20, blank=True, null=True, default='')

    address_provice = models.CharField(max_length=10, blank=True, null=True)
    address_city = models.CharField(max_length=10, blank=True, null=True)
    address_distinct = models.CharField(max_length=10, blank=True, null=True)
    address_stress = models.CharField(max_length=20, blank=True, null=True)

    # Requirement for the post
    degree = models.IntegerField(blank=True, null=True, choices=DEGREE_CHOICES)
    degree_min = models.IntegerField(blank=True, null=True, choices=DEGREE_CHOICES)
    degree_max = models.IntegerField(blank=True, null=True, choices=DEGREE_CHOICES)
    graduatetime_min = models.IntegerField(blank=True, null=True)
    graduatetime_max = models.IntegerField(blank=True, null=True)
    age_min = models.IntegerField(blank=True, null=True)
    age_max = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    recruit_count = models.IntegerField(blank=True, null=True)
    salary_offer = models.CharField(max_length=20, blank=True, null=True, default='')
    observe_time = models.IntegerField(blank=True, null=True)
    interview_location = models.CharField(max_length=30, blank=True, null=True)
    linkman = models.CharField(max_length=10, blank=True, null=True)
    linkman_phone = models.CharField(max_length=15, null=True, blank=True)

    # reserved
    reserved1 = models.CharField(max_length=50, blank=True, null=True, default='')
    reserved2 = models.CharField(max_length=50, blank=True, null=True, default='')

    # table related info
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def save(self, *args, **kwargs):
        if not self.project_name:
            self.project_name = Company.objects.get(pk=self.company).name + '-' + self.name
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return "%s,%s,%s" % (self.name, self.department.name, self.company.name)

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'department'),
    ('2', 'name'),
    ('3', 'project_name'),
    ('4', 'description'),
)

def query_posts_by_args(**kwargs):
    print("================================================================================-")
    draw = int(kwargs.get('draw', [0])[0])
    length = int(kwargs.get('length', [15])[0])
    start = int(kwargs.get('start', [0])[0])
    search_value = kwargs.get('search[value]', [0])[0]
    order_column = kwargs.get('order[0][column]', [0])[0]
    order = kwargs.get('order[0][dir]', [0])[0]

    order_column = ORDER_COLUMN_CHOICES[int(order_column)][1]
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Post.objects.all()
    total = queryset.count()

    # filter and orderby
    if search_value:
        queryset = queryset.filter(models.Q(department__company__name__icontains=search_value) |
                                   models.Q(department__name__icontains=search_value) |
                                   models.Q(name__icontains=search_value) |
                                   models.Q(description__icontains=search_value))

    # ------
    count = queryset.count()

    queryset = queryset.order_by(order_column)[start:start + length]
    # final decoration

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw' : draw,
    }
