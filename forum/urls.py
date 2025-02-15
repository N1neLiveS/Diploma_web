from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
