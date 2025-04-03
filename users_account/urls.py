from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('surf_spots/list/', views.list_surf_spots, name='list_surf_spot'),
    path('login/', views.login_view, name='login'),
    path('surf_spots/paginated/', views.list_surf_spots_paginated, name='list_surf_spots_paginated'),
    path('surf_spots/detail/<int:spot_id>/', views.surf_spot_detail, name='surf_spot_detail'),
    path('surf_spots/<int:spot_id>/add_comment/', views.add_comment, name='add_comment'),
    path('surf_spots/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('surf_spots/edit/<int:post_id>/', views.edit_post, name='edit_post'),
]
