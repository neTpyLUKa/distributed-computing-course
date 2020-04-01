from django.contrib.sites import requests
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)
from src.models import Profile
from rest_framework_simplejwt.tokens import Token, RefreshToken

from src.utils import message_queue


def get_email_and_password(request: Request):
    email = request.data.get('email', '')
    email = BaseUserManager.normalize_email(email)
    email = email.lower()

    password = request.data.get('password', '')
    if not email or not password:
        return None, None

    return email, password


@api_view(["PUT"])
def register_user(request: Request):
    email, password = get_email_and_password(request)
    if email is None:
        return Response({"message": "email or password was not provided"}, HTTP_400_BAD_REQUEST)

    if Profile.exists(email):
        return Response({"message": "user already registered"}, HTTP_400_BAD_REQUEST)

    user = Profile.add(email, password)
    token = RefreshToken.for_user(user=user)
    message_queue.send(email=email, token=str(token))

    # TODO change message to confirm please
    return Response({"message": "successfully created"}, HTTP_200_OK)


class Authorize(TokenObtainPairView):
    def post(self, request: Request, *args):
        request.data['username'] = request.data.get('email', '')
        return super().post(request)


class Verify(TokenVerifyView):
    def post(self, request: Request, *args):
        try:
            super().post(request)
            return Response({"message": "token is valid"}, HTTP_200_OK)
        except InvalidToken:
            return Response({"message": "token is not valid"}, HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    pass


@api_view(["POST"])
def confirm_email(request: Request):
    token = request.query_params.get('token', '')
    if token == '':
        return Response({"message": "token was not provided"}, HTTP_400_BAD_REQUEST)

    try:
        object = RefreshToken(token=token)
    except TokenError as e:
        return Response({"message": str(e)})
    Profile.confirm_email(object['user_id'])
    return Response({"message": "email successfully confirmed"}, HTTP_200_OK)
