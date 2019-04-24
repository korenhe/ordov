from django.urls import path

from .views import CandidateView


app_name = "candidates"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('candidates/', CandidateView.as_view()),
]
