from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks_list, name='tasks_list'),
    path('/<int:task_list_id>/', views.task_detail, name='task_detail'),
    path('my_tasks/', views.my_tasks_view, name='my_tasks'),
]
