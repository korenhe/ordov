# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Interview
from .models import OnDuty

# Register your models here.
admin.site.register(Interview)
admin.site.register(OnDuty)
