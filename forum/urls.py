from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.forum, name='forum'),
    path('create_post/', views.create_post, name='create_post'),
    path('profile_create/', views.profile_create_post, name='profile_create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('reviews/', views.reviews_layout, name='reviews'),
    path('reviews/create_review', views.create_review, name='create_review'),
]
