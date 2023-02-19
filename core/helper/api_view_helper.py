# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
from django.utils import timezone

from core.models import LiveStreamDefaultSettings, LiveStreamOfferSettings, LiveStream
from core.constants import Constant


def check_data_get_serializer(obj, data):
    serializer = obj.get_serializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer


def generate_verify_number():
    # We create a set of digits: {0, 1, .... 9}
    digits = set(range(10))
    # We generate a random integer, 1 <= first <= 9
    first = random.randint(1, 9)
    # We remove it from our set, then take a sample of
    # 3 distinct elements from the remaining values
    last_3 = random.sample(digits - {first}, 3)

    return str(first) + ''.join(map(str, last_3))


def get_time_diff_from_now(time_start):
    diff = timezone.now() - time_start
    result = diff.total_seconds() / 60
    return int(result)


def get_default_settings():
    return LiveStreamDefaultSettings.objects.first()


def get_offer_settings():
    return LiveStreamOfferSettings.objects.filter().order_by('first_value')


def get_time_diff_from_now_second(time_start):
    diff = timezone.now() - time_start
    return int(diff.total_seconds())


def check_and_get_default_live_stream(lives):
    if not lives.exists():
        return LiveStream.objects.filter(status=Constant.LIVE_STATUS_DEFAULT)
    return lives


def set_page_param(request):
    if request.GET.get('page') is None and request.data.get('page', None) is not None:
        request.GET._mutable = True
        request.GET['page'] = request.data.get('page', None)

    return request


def is_exist(name, items):
    exist = False
    for item in items:
        if item == name:
            exist = True

    return exist


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
