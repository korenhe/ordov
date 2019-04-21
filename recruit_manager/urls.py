from django.urls import path

from recruit_manager import views

app_name = 'manager'
urlpatterns = [
    # ex: /manager/
    path('', views.index, name='t_index'), # t_index will be used in template
    path('table/', views.table, name='t_table'), # t_index will be used in template
]
