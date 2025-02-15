from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('welcome', views.welcome, name='welcome'),
    path('welcome/login', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('welcome/last-step', views.last_step, name='last-step'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout')
]
