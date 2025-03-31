from django.contrib import admin
from django.urls import path, include
from users_account import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users_account.urls")),
    path("", views.login_view, name="home"),  # login page as homepage
    path("", include("users_account.urls")),  # include users_account routes directly
]
