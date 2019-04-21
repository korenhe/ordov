# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Candidate

class CandidateAdmin(admin.ModelAdmin):
    list_display=('name', 'gender','identity', 'phone_number','email','degree','major')

# Register your models here.
admin.site.register(Candidate, CandidateAdmin)
