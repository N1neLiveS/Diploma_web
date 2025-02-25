from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('PYTHON_DJANGO', views.python_django, name='python_django'),
]
