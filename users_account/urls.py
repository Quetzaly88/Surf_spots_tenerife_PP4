from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), #route for registration
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
]