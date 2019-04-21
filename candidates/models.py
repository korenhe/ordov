# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .choices import (EDUCATION_CHOICES, BIRTH_YEAR_CHOICES, MAJOR_CHOICES)
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Candidate(models.Model):
    # base info
    username = models.CharField(max_length=4)
#   user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=(("male", "male"), ("female", "female"),), max_length=10, blank=True, null=True)
    birth_year = models.CharField(max_length=4, blank=False, choices=BIRTH_YEAR_CHOICES)
    birth_month= models.CharField(max_length=4)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    identity = models.CharField(max_length=25)

    # social info
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    qq = models.BigIntegerField()
    residence = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=50, blank=False)
    marriaged = models.BooleanField(default=False)

    # education related
    degree = models.CharField(max_length=30)
    major = models.CharField(max_length=30)
    school = models.CharField(max_length=30)

    # table related info
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__ (self):
        return self.username

