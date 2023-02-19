import logging
from rest_framework.exceptions import APIException
from core.helper.response_helper import get_bad_request_response
from core.models import Constant
from core.services.exchange.clients.currency_data import CurrencyDataClient
from core.services.exchange.clients.fixer import FixerClient

logger = logging.getLogger(__name__)


class ExchangeClient:
    provider = None
    client = None

    def __init__(self, provider=Constant.PROVIDER_FIXER):
        self.provider = provider

        self.client = FixerClient()
        if self.provider == Constant.PROVIDER_CURRENCY_DATA:
            self.client = CurrencyDataClient()

    def exchange_rate(self, source_currency, target_currency_list):
        try:
            response = self.client.exchange_rate(source_currency, target_currency_list)
            if response and response['success']:
                return response['rates']
            else:
                return get_bad_request_response(response.error)
        except APIException as exc:
            logger.critical(
                'exchange_rate exception provider: %p  %s: %r',
                self.provider, exc.__class__, exc,
                exc_info=True
            )
            return get_bad_request_response(exc)

    def exchange(self, source_amount, source_currency, target_currency_list):
        try:
            result = {}
            for target_currency in target_currency_list:
                response = self.client.exchange(source_amount, source_currency, target_currency)
                if response and response['success']:
                    result[target_currency] = response['result']
            return result
        except Exception as exc:
            logger.critical(
                'exchange exception provider: %p  %s: %r',
                self.provider, exc.__class__, exc,
                exc_info=True
            )

    def exchange_list(self, start_date=None, end_date=None, source_currency=None, target_currency_list=None):
        try:
            response =  self.client.exchange_list(start_date, end_date, source_currency, target_currency_list)
            if response and response['success']:
                return response['rates']
            else:
                return get_bad_request_response(response.error)
        except Exception as exc:
            logger.critical(
                'exchange_list exception provider: %p  %s: %r',
                self.provider, exc.__class__, exc,
                exc_info=True
            )
