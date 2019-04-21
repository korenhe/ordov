from django.urls import path

from recruit_manager import views

app_name = 'manager'
urlpatterns = [
    # ex: /manager/
    path('', views.index, name='t_index'), # t_index will be used in template
    path('candidates/', views.CandidateTable.as_view(), name='t_candidates'),
    path('interviews/', views.InterviewTable.as_view(), name='t_interviews'),
]
