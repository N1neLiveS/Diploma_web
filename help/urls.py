from django.urls import path
from . import views

urlpatterns = [
    path('', views.helps_forum, name='help'),
    path('create_question', views.create_question, name='create_question'),
    path('post/<int:question_id>/', views.question_detail, name='question_detail'),
]