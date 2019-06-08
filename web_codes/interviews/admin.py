# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Interview
from .models import InterviewLogCommon

from .models import InterviewSub_Appointment, InterviewSub_Appointment_Agree
from .models import InterviewSub_Interview, InterviewSub_Interview_Pass
from .models import InterviewSub_Offer, InterviewSub_Offer_Agree
from .models import InterviewSub_Payback, InterviewSub_Payback_Finish

from .models import OnDuty

# Register your models here.
admin.site.register(Interview)
admin.site.register(InterviewLogCommon)

admin.site.register(InterviewSub_Appointment)
admin.site.register(InterviewSub_Appointment_Agree)

admin.site.register(InterviewSub_Interview)
admin.site.register(InterviewSub_Interview_Pass)

admin.site.register(InterviewSub_Offer)
admin.site.register(InterviewSub_Offer_Agree)

admin.site.register(InterviewSub_Payback)
admin.site.register(InterviewSub_Payback_Finish)

admin.site.register(OnDuty)
