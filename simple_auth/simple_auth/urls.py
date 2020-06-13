"""simple_auth URL Configuration

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
import os

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from src.views import register_user, Authorize, CustomTokenRefreshView, Verify, confirm_email, register_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register_user', register_user),
    path('register_admin', register_admin),
    path('authorize', Authorize.as_view()),
    path('refresh', CustomTokenRefreshView.as_view()),
    # path('verify', Verify.as_view()),
    path('confirm_email', confirm_email),
]

if os.environ.get("AUTH_GRPC_MODE"):
    import sys

    sys.path.insert(0, "..")

    from src.handlers import grpc_handlers as auth_grpc_handlers


    def grpc_handlers(server):
        auth_grpc_handlers(server)
