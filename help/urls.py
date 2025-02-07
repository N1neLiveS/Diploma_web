from django.urls import path
from . import views

urlpatterns = [
    path('', views.helps, name='help'),
    path('create_post', views.create_question, name='create_question'),
]