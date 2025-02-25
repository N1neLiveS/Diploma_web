from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.forum, name='forum'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]
