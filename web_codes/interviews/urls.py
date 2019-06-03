from django.urls import include, path

from rest_framework import routers
from .views import InterviewSub_InterviewViewSet, InterviewSub_Interview_PassViewSet
from .views import InterviewSub_OfferViewSet, InterviewSub_Offer_AgreeViewSet

router = routers.DefaultRouter()
router.register(r'interviewsub', InterviewSub_InterviewViewSet)
router.register(r'interviewsub_pass', InterviewSub_Interview_PassViewSet)
router.register(r'offersub', InterviewSub_OfferViewSet)
router.register(r'offersub_agree', InterviewSub_Offer_AgreeViewSet)

app_name = "interviews"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('api/', include(router.urls)),
]
