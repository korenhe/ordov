# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .choices import (EDUCATION_CHOICES, BIRTH_YEAR_CHOICES, MAJOR_CHOICES, MARRIAGE_CHOICES, EDUCATION_TYPE_CHOICES)
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
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
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
    degree = models.CharField(max_length=30, blank=True, null=True)
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

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()

    school = models.CharField(max_length=50)
    college = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    degree = models.CharField(max_length=50, choices=EDUCATION_CHOICES)
    edu_type = models.CharField(max_length=50, choices=EDUCATION_TYPE_CHOICES, null=True)

    instructor = models.CharField(max_length=50, null=True)
    instructor_phone = PhoneNumberField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.degree
