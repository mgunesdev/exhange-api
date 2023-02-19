# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from core.decorators import check_auth
from core.helper.response_helper import get_detail_error_response, get_detail_successfully_response
from core.permissions import IsOwner
from rest_framework.generics import (
    CreateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from .serializers import *

User = get_user_model()


def change_password_user(user, new_password):
    user.set_password(new_password)
    user.is_active = True
    user.last_login = timezone.now()
    user.save()


def re_authenticate_user(user):
    authenticate(username=user.username, password=user.password)
    token, created = Token.objects.get_or_create(user=user)

    user.last_login = timezone.now()
    user.is_active = True
    user.save(update_fields=["last_login", "is_active"])

    return token.key


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.filter(Q(email=serializer.validated_data['email']))
            if not user.exists:
                return get_detail_error_response(
                    'register_error', ErrorMessages.ERROR_ACCOUNT_USER_CHECK, serializer.errors
                )
            user = user.first()
            token_info = re_authenticate_user(user)

            new_data = {
                "token": token_info,
                "user_info": UserMeSerializer(user, context={'request': request}).data
            }

            return get_detail_successfully_response(new_data)

        return get_detail_error_response('register_error', ErrorMessages.ERROR_VALIDATION, serializer.errors)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token_info = re_authenticate_user(user)

            new_data = {
                "token": token_info,
                "user_info": UserMeSerializer(user, context={'request': request}).data
            }

            return get_detail_successfully_response(new_data)

        return get_detail_error_response('login_error', ErrorMessages.ERROR_VALIDATION, serializer.errors)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @check_auth
    def post(self, request, *args, **kwargs):
        new_data = {
            "status": True,
        }

        return get_detail_successfully_response(new_data)


class UserDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @check_auth
    def post(self, request, *args, **kwargs):
        user = request.user
        user.auth_token.delete()
        user.status = Constant.STATUS_PASSIVE
        user.is_active = False
        user.save()
        new_data = {
            "status": True,
        }

        return get_detail_successfully_response(new_data)


class UserMeAPIView(CreateAPIView):
    model = User
    permission_classes = [IsOwner]
    serializer_class = UserMeSerializer
    queryset = User.objects.all()

    @check_auth
    def post(self, request, *args, **kwargs):
        return get_detail_successfully_response(UserMeSerializer(request.user, context={'request': request}).data)
