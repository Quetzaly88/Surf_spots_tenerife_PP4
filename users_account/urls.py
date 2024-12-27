from django.urls import path
from . import views
from .views import create_surf_spot


urlpatterns = [
    path('register/', views.register, name='register'),  # route for registration
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('api/surf_spots/create', views.create_surf_spot, name='create_surf_spot'), 
    path('api/surf_spots/list', views.list_surf_spots, name='list_surf_spot'), 
]