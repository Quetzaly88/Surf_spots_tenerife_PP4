from django.urls import path
from . import views
from .views import create_surf_spot


urlpatterns = [
    path('register/', views.register, name='register'),  # route for registration
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
]

urlpatterns += [
    path('api/surf_spots/create', create_surf_spot, name='create_surf_spot'), 
]