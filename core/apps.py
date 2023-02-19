# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class BaseAppConfig(AppConfig):
    name = 'core'
    verbose_name = 'EXCHANGE API'

    def ready(self):
        pass
