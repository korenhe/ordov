from django.urls import include, path

from rest_framework import routers
from .views import InterviewSub_InterviewViewSet, InterviewSub_Interview_PassViewSet

router = routers.DefaultRouter()
router.register(r'interviewsub', InterviewSub_InterviewViewSet)
router.register(r'interviewsub_pass', InterviewSub_Interview_PassViewSet)

app_name = "interviews"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('api/', include(router.urls)),
]
