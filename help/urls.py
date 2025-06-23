from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.helps_forum, name='help'),
    path('create_question', views.create_question, name='create_question'),
    path('<int:question_id>', views.question_detail, name='question_detail'),
    path('<int:question_id>/delete', views.question_delete, name='question_delete'),
    path('<int:question_id>/update_status', views.question_update_status, name='question_update_status'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]