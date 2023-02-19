# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from rest_framework_jwt.compat import PasswordField
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as CustomUserSerializer, UserCreatePasswordRetypeSerializer, \
    TokenSerializer
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError
)

from rest_framework import serializers
from core.helper.response_helper import ErrorMessages
from core.constants import Constant

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'username', 'password')


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ('email', 'username', 'password')


class UserLoginSerializer(ModelSerializer):
    username = CharField(allow_blank=True, required=False)
    email = EmailField(allow_blank=True, required=False, label='Email Address')
    password = PasswordField(allow_blank=True, required=False, label='Password')

    class Meta(TokenSerializer.Meta):
        model = User
        fields = [
            'username',
            'password',
            'email',
        ]

    def validate(self, data):
        username = data.get("username", None)
        email = data.get("email", None)
        password = data["password"]
        if not email and not username:
            raise ValidationError(ErrorMessages.ERROR_ACCOUNT_NOT_EMPTY)

        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        )
        user_obj = None
        if user.exists():
            user_obj = user.first()
            if user_obj.status == Constant.STATUS_PASSIVE:
                raise ValidationError(ErrorMessages.ERROR_ACCOUNT_DELETE_CHECK)
            if not user_obj.check_password(password):
                raise ValidationError(ErrorMessages.ERROR_ACCOUNT_PASSWORD_NOT_FOUND)

        data['user'] = user_obj

        return data


class UserMeSerializer(CustomUserSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'status'
        ]
        depth = 1