# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import time
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from core.constants import Constant


class CustomUserManager(UserManager):

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )


def _createHash():
    message = str(time.time()).encode()
    code = hashlib.sha256(message).hexdigest()[:16]
    return code


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(_("Kayıt Tarihi"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    deleted = models.BooleanField(_("Silindi Mi ?"), blank=True, default=False, editable=False)
    deleted_at = models.DateTimeField(_("Silinme Tarihi"), blank=True, null=True, editable=False)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()


class MinNameValidator(RegexValidator):
    regex = r'^.{4,}$'
    message = _(
        'Enter a valid username. This value must be at least 4 characters.'
    )
    flags = 0


class User(AbstractUser, TimeStampMixin):
    username_validator = UnicodeUsernameValidator()
    username_min_length_validator = MinNameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, username_min_length_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("E-posta"), unique=True, null=True, blank=True)
    status = models.SmallIntegerField(
        _("Durum"),
        choices=Constant.STATUS_CHOICES,
        default=Constant.STATUS_ACTIVE
    )

    register_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(blank=True, null=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username + " / " + str(self.is_active)

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "users"


class MyAuthBackend(object):

    def authenticate(self, email, password):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(sys_id=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
