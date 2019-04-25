from django.urls import path

from .views import ResumeView


app_name = "candidates"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('resumes/', ResumeView.as_view()),
]
