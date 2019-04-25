# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')

    def __str__ (self):
        return self.user.username
