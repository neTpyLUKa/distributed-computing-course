from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from src.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from src.utils import message_queue_email, message_queue_sms

from proto.auth_pb2 import (
    Admin,
    Token,
)

def get_token(request: Request):
    return request.META.get("HTTP_AUTHORIZATION", '').split("Bearer ")[-1]

def is_admin(request: Request):
    token = get_token(request)
    try:
        token = UntypedToken(token)
        profile = Profile.objects.get(user_id=token["user_id"])
        return profile.role == Admin
    except TokenError as e:
        print(e)

    return False


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

    phone = request.data.get('phone', '')
    if phone != '':
        message_queue_sms.send(address=phone, token=str(token))
        return Response({"message": "Check your phone to continue registration"}, HTTP_200_OK)
    else:
        message_queue_email.send(address=email, token=str(token))
        return Response({"message": "Check your mailbox to continue registration"}, HTTP_200_OK)


@api_view(["PUT"])
def register_admin(request: Request):
    if not is_admin(request):
        return Response({"message": "Wrong token or not provided or not enough privileges"}, HTTP_401_UNAUTHORIZED)

    email, password = get_email_and_password(request)
    if email is None:
        return Response({"message": "email or password was not provided"}, HTTP_400_BAD_REQUEST)

    if Profile.exists(email):
        return Response({"message": "user already registered"}, HTTP_400_BAD_REQUEST)

    user = Profile.add(email, password, role=Admin, is_active=True)
    user.save()

    return Response({"message": "Admin successfully registered"}, HTTP_200_OK)


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


@api_view(["GET"])
def confirm_email(request: Request):
    token = request.query_params.get('token', '')
    if token == '':
        return Response({"message": "token was not provided"}, HTTP_400_BAD_REQUEST)

    try:
        object = RefreshToken(token=token)
    except TokenError as e:
        return Response({"message": str(e)})
    Profile.confirm_email(object['user_id'])
    return Response({"message": "registration complete"}, HTTP_200_OK)
