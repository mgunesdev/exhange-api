# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, \
    HTTP_403_FORBIDDEN, \
    HTTP_200_OK, HTTP_501_NOT_IMPLEMENTED, HTTP_409_CONFLICT
from django.utils.translation import gettext_lazy as _, ugettext
from core.models import User


class SuccessMessages:
    DELETED_SUCCESSFULLY = _("Başarı ile silindi!")
    UPDATED_SUCCESSFULLY = _("Başarı ile güncellendi!")
    CREATED_SUCCESSFULLY = _("Başarı ile oluşturuldu!")


class ErrorMessages:
    ERROR_UNKNOWN = _("Bilinmeyen bir hata oluştu!")
    ERROR_NOT_FOUND = _("Böyle bir kayıt bulunamadı!")
    ERROR_NOT_OWNER = _("Bu işlemi yapmaya yetkiniz yok!")
    ERROR_NOT_LOGIN = _("Bu işlemi yapabilmek için giriş yapmalısınız!")
    ERROR_MISSING_INFO = _("Eksik alan!")
    ERROR_ALREADY_DONE = _("Bu işlem zaten yapılmış!")
    ERROR_VALIDATION = _("Bilgileri kontrol ederek tekrar deneyiniz!")

    ERROR_ACCOUNT_NOT_EMPTY = _("Kullanıcı adı ve email boş olamaz!")
    ERROR_ACCOUNT_DELETE_CHECK = _(
        "Hesabınız silinmiştir. Eğer tekrar açmak isterseniz lütfen bizimle iletişime geçin.")
    ERROR_ACCOUNT_USERNAME_AND_EMAIL_CHECK = _('Kullanıcı adı ya da eposta zaten kullanılıyor.')
    ERROR_ACCOUNT_PASSWORD_NOT_FOUND = _("Şifreniz Hatalı!")
    ERROR_ACCOUNT_INCORRECT_PASSWORD = _("Şifreler Uyuşmadı!")
    ERROR_ACCOUNT_INCORRECT_OLD_PASSWORD = _("Eski Şifre Uyuşmadı!")
    ERROR_ACCOUNT_INCORRECT_PARAMETERS = _("Parametreler Uyuşmadı!")
    ERROR_ACCOUNT_USER_CHECK = _("Kullanıcı Bulunamadı!")
    ERROR_ACCOUNT_USER_VERIFIED = _("Lüften eposta ve telefon numaranızı doğrulayınız!")
    ERROR_ACCOUNT_EMAIL_NOT_FOUND = _("Eposta bulunamadı!")
    ERROR_ACCOUNT_PHONE_CHECK = _("Telefon numarası bulunamadı!")
    ERROR_ACCOUNT_PHONE_VERIFY_CHECK = _("Telefon numarası zaten onaylanmış!")
    ERROR_ACCOUNT_EMAIL_OR_CODE_CHECK = _("Eposta ya da onay kodu bulunamadı!")
    ERROR_ACCOUNT_VERIFY_CODE_MISMATCH = _("Onay kodu eşleşmedi!")



class ErrorCodes:
    NOT_LOGIN_CODE = 10001
    NOT_OWNER = 10002
    NOT_FOUND = 10003
    BAD_REQUEST = 10004
    UNKNOWN = 10005
    CONFLICT = 10006


class ResponseInfo(object):
    STATUS_SUCCESS = 'SUCCESS'
    STATUS_ERROR = 'ERROR'

    def __init__(self, user=None, **args):
        is_error = args.get('is_error', False)
        is_create = args.get('is_create', False)
        is_paginate = args.get('is_paginate', False)
        page = args.get('page', 1)
        status_code = args.get('status_code', 200)
        error_title = args.get('error_title', None)
        error_message = args.get('error_message', None)
        total_items = args.get('total_items', 0)
        next_page_url = args.get('next', None)
        success_title = args.get('success_title', None)
        success_message = args.get('success_message', None)
        data = args.get('data', None)
        extra = args.get('extra', '')

        last_page = args.get('last_page', False)
        if next_page_url is None:
            last_page = True

        status = {
            "code": status_code,
            "statusTraceCode": self.STATUS_SUCCESS,
        }

        if is_error:
            status = {
                "code": status_code,
                "statusTraceCode": self.STATUS_ERROR,
                "popup": {
                    "title": error_title,
                    "message": error_message,
                    "type": "error"
                }
            }
            data = None

        if is_paginate:
            data = {
                "PaginatedResponseData": {
                    "totalItems": total_items,
                    "currentPage": page,
                    "lastPage": last_page,
                    "nextPageUrl": next_page_url,
                    "extra": extra,
                    "data": data,
                }
            }

        if is_create:
            data = {
                "popup": {
                    "title": success_title,
                    "message": success_message,
                    "type": "success"
                }
            }

        self.response = {
            "status": status,
            "data": data,
        }


def is_authenticated(request):
    return bool(request.user and request.user.is_authenticated)


def is_owner(request, model):
    if type(model) is User:
        return model == request.user or model == request.user.parent
    return request.user == model.user or model.user == request.user.parent


def get_not_authenticated_response():
    response = ResponseInfo(
        is_error=True,
        error_title='verified_error',
        error_message=ErrorMessages.ERROR_NOT_LOGIN,
        status_code=HTTP_400_BAD_REQUEST
    ).response

    return Response(response, status=HTTP_200_OK)

def get_not_verified_response():
    response = ResponseInfo(
        is_error=True,
        error_title='authenticate_error',
        error_message=ErrorMessages.ERROR_ACCOUNT_USER_VERIFIED,
        status_code=HTTP_400_BAD_REQUEST
    ).response

    return Response(response, status=HTTP_200_OK)

def get_not_owner_response():
    response = ResponseInfo(
        is_error=True,
        error_title='not_owner_error',
        error_message=ErrorMessages.ERROR_NOT_OWNER,
        status_code=HTTP_403_FORBIDDEN
    ).response

    return Response(response, status=HTTP_200_OK)


def get_not_found_response():
    response = ResponseInfo(
        is_error=True,
        error_title='not_found_error',
        error_message=ErrorMessages.ERROR_NOT_FOUND,
        status_code=HTTP_400_BAD_REQUEST
    ).response

    return Response(response, status=HTTP_200_OK)


def get_bad_request_response(exception):
    exp_list = list(exception.detail.keys())
    title = exp_list[0]
    message = exception.detail.get(title)[0]
    response = ResponseInfo(
        is_error=True,
        error_title=title,
        error_message=message,
        status_code=HTTP_400_BAD_REQUEST
    ).response

    return Response(response, status=HTTP_200_OK)


def get_custom_bad_request_response(title, message):
    response = ResponseInfo(
        is_error=True,
        error_title=title,
        error_message=message,
        status_code=HTTP_400_BAD_REQUEST
    ).response

    return Response(response, status=HTTP_200_OK)


def get_custom_bad_request_exc_response(title, exception):
    message = exception.detail[0]
    response = ResponseInfo(
        is_error=True,
        error_title=title,
        error_message=message,
        status_code=HTTP_400_BAD_REQUEST
    ).response

    return Response(response, status=HTTP_200_OK)

def get_bad_request_key_response(key):
    response = ResponseInfo(
        is_error=True,
        error_title=key,
        error_message=ErrorMessages.ERROR_MISSING_INFO,
        status_code=HTTP_400_BAD_REQUEST
    ).response

    return Response(response, status=HTTP_200_OK)


def get_bad_request_message_response(message):
    response = ResponseInfo(
        is_error=True,
        error_title='bad_request_error',
        error_message=message,
        status_code=HTTP_400_BAD_REQUEST
    ).response

    return Response(response, status=HTTP_200_OK)


def get_unknown_error_response():
    response = ResponseInfo(
        is_error=True,
        error_title='unknown_error',
        error_message=ErrorMessages.ERROR_UNKNOWN,
        status_code=HTTP_501_NOT_IMPLEMENTED
    ).response

    return Response(response, status=HTTP_200_OK)


def get_deleted_successfully_response():
    response = ResponseInfo(
        success_message=SuccessMessages.DELETED_SUCCESSFULLY,
        success_title=SuccessMessages.DELETED_SUCCESSFULLY,
        status_code=HTTP_200_OK,
    ).response

    return Response(response, status=HTTP_200_OK)


def get_created_successfully_response(model):
    response = ResponseInfo(
        success_message=SuccessMessages.UPDATED_SUCCESSFULLY,
        success_title=SuccessMessages.UPDATED_SUCCESSFULLY,
        status_code=HTTP_200_OK,
        data=model
    ).response

    return Response(response, status=HTTP_201_CREATED)


def get_successfully_response(model):
    response = ResponseInfo(
        success_message=SuccessMessages.UPDATED_SUCCESSFULLY,
        success_title=SuccessMessages.UPDATED_SUCCESSFULLY,
        status_code=HTTP_200_OK,
        data=model
    ).response

    return Response(response, status=HTTP_200_OK)


def get_updated_successfully_response(model):
    response = ResponseInfo(
        success_message=SuccessMessages.UPDATED_SUCCESSFULLY,
        success_title=SuccessMessages.UPDATED_SUCCESSFULLY,
        status_code=HTTP_200_OK,
        data=model
    ).response

    return Response(response, status=HTTP_200_OK)


def get_detail_successfully_response(model):
    response = ResponseInfo(
        data=model,
        status_code=HTTP_200_OK,
    ).response

    return Response(response)


def get_detail_error_response(title, message_type, errors=None):
    message = message_type
    if errors:
        message = get_error_message(errors, message_type)

    response = ResponseInfo(
        is_error=True,
        error_title=title,
        error_message=message,
        status_code=HTTP_400_BAD_REQUEST
    ).response

    return Response(response, status=HTTP_200_OK)


def get_list_successfully_response(params, data):
    response = ResponseInfo(
        data=data["results"],
        status_code=HTTP_200_OK,
    ).response

    return Response(response, status=HTTP_200_OK)


def get_paginated_response(params, data, extra=None):
    response = ResponseInfo(
        data=data["results"],
        status_code=HTTP_200_OK,
        is_paginate=True,
        page=int(params.get("page", 1)),
        total_items=data.get("count"),
        next=data.get('next'),
        extra=extra
    ).response

    return Response(response, status=HTTP_200_OK)


def get_error_message(errors, message_type=ErrorMessages.ERROR_VALIDATION):
    message = message_type

    if isinstance(errors, dict):
        for key in errors:
            for msg in errors[key]:
                message = "{}".format(msg)

            if key == 'non_field_errors':
                message = "{}".format(errors[key][0])

    return message
