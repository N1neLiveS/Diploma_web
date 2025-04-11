from django.urls import path
from . import views

urlpatterns = [
    path('', views.me, name='me'),
    path('settings', views.settings_account, name='settings_account')
]