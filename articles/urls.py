from django.urls import path, include
from . import views

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('', views.articles_main, name='articles'),
    path('create_article/', views.create_article, name='create_article'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
]
