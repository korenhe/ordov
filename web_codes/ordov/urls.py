"""ordov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from candidates import views as candidatesViews
from resumes import views as resumesViews
from accounts import views as accountsViews
from companies import views as companiesViews
from interviews import views as interviewsViews

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'resumes', resumesViews.ResumeViewSet)
router.register(r'candidates', candidatesViews.CandidateViewSet)
router.register(r'posts', companiesViews.PostViewSet)
router.register(r'interviews', interviewsViews.InterviewViewSet)

urlpatterns = [
    path('accounts/signup/', accountsViews.signup, name='signup'),
    path('accounts/login/', accountsViews.MyLoginView.as_view(), name='login'),
    path('accounts/', include('allauth.urls')),
    path('candidates/resume/update', candidatesViews.updateResume, name='candidate_update_resume'),
    path('candidates/resume/success', candidatesViews.apply_success, name='candidate_apply_success'),

    path('admin/', admin.site.urls),

    path('', include('landing_page.urls')),

    path('manager/', include('recruit_manager.urls'), name='manager'),
    path('company/', include('recruit_company.urls'), name='company'),
    path('applicant/', include('recruit_applicant.urls'), name='applicant'),

    path('api/', include(router.urls)),
]
