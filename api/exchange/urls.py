# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from api.exchange.views import ExchangeRatesAPIView, ExchangeConvertAPIView, ExchangeListAPIView

app_name = "exchange"
urlpatterns = [
    url(r'^rates/$', ExchangeRatesAPIView.as_view(), name='api-exchange-rates'),
    url(r'^convert/$', ExchangeConvertAPIView.as_view(), name='api-exchange-convert'),
    url(r'^list/$', ExchangeListAPIView.as_view(), name='api-exchange-list'),


]
