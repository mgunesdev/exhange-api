# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from api.account.views import *

urlpatterns = [
    url(r'^register/$', UserCreateAPIView.as_view(), name='api-user-register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='api-user-login'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='api-user-logout'),
    url(r'^delete/$', UserDeleteAPIView.as_view(), name='api-user-delete'),
    url(r'^me/$', UserMeAPIView.as_view(), name='api-user-me')
]
