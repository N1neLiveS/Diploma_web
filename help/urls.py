from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.helps_forum, name='help'),
    path('create_question', views.create_question, name='create_question'),
    path('/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]