"""onlineshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from simple_auth.views import register_user, Authorize, Verify, CustomTokenRefreshView
from backend.views import ProductView
from backend.views import ListProductView
from backend.views import InitView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    token_verify)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product', ProductView.as_view()),
    path('products', ListProductView.as_view()),
    path('init', InitView),
    path('register', register_user),
    path('authorize', Authorize.as_view()),
    path('refresh', CustomTokenRefreshView.as_view()),
    path('verify', Verify.as_view())

]
