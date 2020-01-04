from django.urls import include, path

from rest_framework import routers
from .views import InterviewSub_AppointmentViewSet
from .views import InterviewSub_InterviewViewSet, InterviewSub_Interview_PassViewSet
from .views import InterviewSub_OfferViewSet, InterviewSub_Offer_AgreeViewSet
from .views import InterviewSub_ProbationViewSet, InterviewSub_Probation_FailViewSet
from .views import InterviewSub_PaybackViewSet, InterviewSub_Payback_FinishViewSet
from .views import InterviewSub_TerminateViewSet
from interviews import views

router = routers.DefaultRouter()

router.register(r'appointment_sub', InterviewSub_AppointmentViewSet)

router.register(r'interview_sub', InterviewSub_InterviewViewSet)
router.register(r'interview_sub_pass', InterviewSub_Interview_PassViewSet)

router.register(r'offer_sub', InterviewSub_OfferViewSet)
router.register(r'offer_sub_agree', InterviewSub_Offer_AgreeViewSet)

router.register(r'probation_sub', InterviewSub_ProbationViewSet)
router.register(r'probation_sub_fail', InterviewSub_Probation_FailViewSet)

router.register(r'payback_sub', InterviewSub_PaybackViewSet)
router.register(r'payback_sub_finish', InterviewSub_Payback_FinishViewSet)

router.register(r'terminate_sub', InterviewSub_TerminateViewSet)

app_name = "interviews"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('api/', include(router.urls)),
    path('sub/offer/<int:interview_id>/', views.interviewsub_get_offer_detail, name='t_interviewsub_offer'),
]
