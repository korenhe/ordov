from django.urls import path

from recruit_manager import views
from resumes import views as resumesViews
from companies import views as companiesViews
from interviews import views as interviewsViews

app_name = 'app_manager'
urlpatterns = [
    # ex: /manager/
    path('', views.index, name='t_index'), # t_index will be used in template
    path('upload/', views.upload, name='t_upload'),
    path('candidates/', views.CandidateTable.as_view(), name='t_candidates'),

    path('interviews/', interviewsViews.InterviewTable.as_view(), name='t_interviews'),
    path('interview-api/<int:candidate_id>', views.interview_api, name='t_interview_api'),
    path('interview-result/<int:candidate_id>', views.interview_result, name='t_interview_result'),

    path('resumes/', resumesViews.ResumeTable.as_view(), name='t_resumes'),
    path('multi/', resumesViews.MultiTable.as_view(), name='t_multi'),
    path('composite/', resumesViews.CompositeTable.as_view(), name='t_composite'),
    path('resumes/<int:pk>', resumesViews.ResumeDetail.as_view(), name='t_resume'),
    path('posts/', companiesViews.PostTable.as_view(), name='t_posts'),
]
