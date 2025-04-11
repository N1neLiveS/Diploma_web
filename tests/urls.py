from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='tests'),
    path('/<int:test_id>/take/', views.take_test, name='take_test'),
]