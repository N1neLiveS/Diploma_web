from django.urls import path
from . import views

urlpatterns = [
    path('', views.quests, name='quests'),
    path('lectures', views.lectures, name='lectures'),
    path('QUEST_PYTHON_BASIC', views.python_basic, name='python_basic')
]
