"""surf_spots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import (
    path,
    include,
)  # include function allows to connect the urls of the users_account app to the main urls.py
from users_account import views  # import views directly


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users_account.urls")),
    path("", views.login_view, name="home"),  # login page as homepage
    path("", include("users_account.urls")),  # include users_account routes directly
]
