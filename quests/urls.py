from django.urls import path
from . import views

urlpatterns = [
    path('', views.quests, name='quests'),
    path('lectures', views.lectures_home, name='lectures'),
    path('lectures/<int:lecture_id>/', views.lecture_detail, name='lecture_detail'),
    path('QUEST_PYTHON_BASIC', views.python_basic, name='python_basic')
]
