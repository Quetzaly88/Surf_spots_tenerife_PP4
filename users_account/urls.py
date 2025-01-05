from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # route for registration
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'), #correct
    path('surf_spots/list/', views.list_surf_spots, name='list_surf_spot'),   
    path('', views.login_view, name='login'), #Avoid no conflicting patterns are overriding home route.
    path('surf_spots/paginated/', views.list_surf_spots_paginated, name='list_surf_spots_paginated'),
    path('surf_spots/detail/<int:spot_id>/', views.surf_spot_detail, name='surf_spot_detail'),
    path('surf_spots/detail/<int:spot_id>/', views.surf_spot_detail, name='surf_spot_detail'),
    path('surf_spots/<int:spot_id>/add_comment/', views.add_comment, name='add_comment'),
]