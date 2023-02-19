# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.contrib import admin


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]

        super(ListAdminMixin, self).__init__(model, admin_site)


app = apps.get_app_config('core')
for model_name, model in app.models.items():
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    admin.site.register(model, admin_class)
