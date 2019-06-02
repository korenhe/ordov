# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Interview
from .models import InterviewSub_Interview, InterviewSub_Interview_Pass
from .models import OnDuty

# Register your models here.
admin.site.register(Interview)
admin.site.register(InterviewSub_Interview)
admin.site.register(InterviewSub_Interview_Pass)
admin.site.register(OnDuty)
