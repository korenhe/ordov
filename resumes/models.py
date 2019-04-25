# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .choices import (EDUCATION_CHOICES, BIRTH_YEAR_CHOICES, MAJOR_CHOICES)
from django.utils.encoding import python_2_unicode_compatible
from candidates.models import Candidate

# Create your models here.

@python_2_unicode_compatible
class Resume(models.Model):
    # The Resume would be linked to a candidate afterwards
    # This resume would
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, blank=True)
    resume_id = models.IntegerField()
    visible = models.BooleanField(default=False) 
    # base info
    username = models.CharField(max_length=4)
    gendor = models.CharField(choices=(("male", "male"), ("female", "female"),), max_length=10, blank=True, null=True)
    birth_year = models.CharField(max_length=4, blank=True, null=True, choices=BIRTH_YEAR_CHOICES)
    birth_month= models.CharField(max_length=4, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    identity = models.CharField(max_length=25, blank=True, null=True)

    # social info
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    qq = models.BigIntegerField(null=True, blank=True)
    residence = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    marriaged = models.BooleanField(default=False)

    # education related
    degree = models.CharField(max_length=30, blank=True, null=True)
    major = models.CharField(max_length=30, blank=True, null=True)
    school = models.CharField(max_length=30, blank=True, null=True)

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

    def __str__(self):
        return self.degree
