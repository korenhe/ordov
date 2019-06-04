from django.urls import include, path

from rest_framework import routers
from .views import InterviewSub_AppointmentViewSet, InterviewSub_Appointment_AgreeViewSet
from .views import InterviewSub_InterviewViewSet, InterviewSub_Interview_PassViewSet
from .views import InterviewSub_OfferViewSet, InterviewSub_Offer_AgreeViewSet

router = routers.DefaultRouter()

router.register(r'appointment_sub', InterviewSub_AppointmentViewSet)
router.register(r'appointment_sub_agree', InterviewSub_Appointment_AgreeViewSet)

router.register(r'interview_sub', InterviewSub_InterviewViewSet)
router.register(r'interview_sub_pass', InterviewSub_Interview_PassViewSet)

router.register(r'offer_sub', InterviewSub_OfferViewSet)
router.register(r'offer_sub_agree', InterviewSub_Offer_AgreeViewSet)

app_name = "interviews"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('api/', include(router.urls)),
]
