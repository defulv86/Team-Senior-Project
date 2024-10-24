from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('testpage/', views.testpage, name='testpage'),
]
