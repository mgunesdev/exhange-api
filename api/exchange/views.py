from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView

from api.exchange.serializers import ExchangeRatesSerializer, ExchangeConvertSerializer, ExchangeListSerializer
from core.constants import Constant
from core.decorators import check_auth
from core.helper.response_helper import get_bad_request_response, get_detail_error_response, ErrorMessages, \
    get_successfully_response
from rest_framework.exceptions import APIException

from core.services.exchange.client import ExchangeClient


class ExchangeRatesAPIView(CreateAPIView):
    serializer_class = ExchangeRatesSerializer

    @check_auth
    def post(self, request, *args, **kwargs):
        serializer = ExchangeRatesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data
                source_currency = validated_data.get('source_currency')
                target_currency_list = validated_data.get('target_currency_list')

                client = ExchangeClient(provider=int(request.headers.get('X-PROVIDER', Constant.PROVIDER_FIXER)))
                result = client.exchange_rate(
                    source_currency=source_currency,
                    target_currency_list=target_currency_list
                )

                response = {
                    "result": result,
                }

                return get_successfully_response(response)
            except APIException as exp:
                return get_bad_request_response(exp)
        return get_detail_error_response('exchange_rates_error', ErrorMessages.ERROR_VALIDATION,
                                         serializer.errors)


class ExchangeConvertAPIView(CreateAPIView):
    serializer_class = ExchangeConvertSerializer

    @check_auth
    def post(self, request, *args, **kwargs):
        serializer = ExchangeConvertSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data
                source_amount = validated_data.get('source_amount')
                source_currency = validated_data.get('source_currency')
                target_currency_list = validated_data.get('target_currency_list')

                client = ExchangeClient(provider=int(request.headers.get('X-PROVIDER', Constant.PROVIDER_FIXER)))
                result = client.exchange(
                    source_amount=source_amount,
                    source_currency=source_currency,
                    target_currency_list=target_currency_list
                )

                return get_successfully_response({
                    "result": result,
                })
            except APIException as exp:
                return get_bad_request_response(exp)
        return get_detail_error_response('exchange_convert_error', ErrorMessages.ERROR_VALIDATION,
                                         serializer.errors)


class ExchangeListAPIView(CreateAPIView):
    serializer_class = ExchangeListSerializer

    @check_auth
    def post(self, request, *args, **kwargs):
        serializer = ExchangeListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data

                start_date = validated_data.get('start_date', None)
                end_date = validated_data.get('end_date', None)
                source_currency = validated_data.get('source_currency', None)
                target_currency_list = validated_data.get('target_currency_list', None)

                client = ExchangeClient(provider=int(request.headers.get('X-PROVIDER', Constant.PROVIDER_FIXER)))
                result = client.exchange_list(
                    start_date=start_date,
                    end_date=end_date,
                    source_currency=source_currency,
                    target_currency_list=target_currency_list
                )

                response = {
                    "result": result,
                }

                return get_successfully_response(response)
            except APIException as exp:
                return get_bad_request_response(exp)
        return get_detail_error_response('exchange_list_error', ErrorMessages.ERROR_VALIDATION,
                                         serializer.errors)

