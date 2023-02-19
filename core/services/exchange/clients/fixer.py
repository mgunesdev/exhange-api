import datetime

from decouple import config
from core.services.exchange.clients.base import BaseClient


class FixerClient(BaseClient):
    api_key = config('FIXER_API_KEY')
    url = "https://api.apilayer.com/fixer/{}?{}"
    method = None

    def __init__(self):
        self.headers = {
            "apikey": self.api_key
        }

    def exchange_rate(self, source_currency, target_currency_list):
        self.method = 'latest'
        self.payload = {
            'base': source_currency,
            'symbols': ','.join(target_currency_list)
        }

        response = self.request()
        return response

    def exchange(self, source_amount, source_currency, target_currency):
        self.method = 'convert'
        self.payload = {
            'to': source_currency,
            'from': target_currency,
            'amount': source_amount,
            'date': datetime.datetime.now().strftime("%Y-%m-%d")
        }

        response = self.request()
        return response

    def exchange_list(self, start_date=None, end_date=None, source_currency=None, target_currency_list=None):
        self.method = 'timeseries'
        self.payload = {}

        if start_date:
            self.payload['start_date'] = start_date

        if end_date:
            self.payload['end_date'] = end_date

        if source_currency:
            self.payload['base'] = source_currency

        if target_currency_list:
            self.payload['symbols'] = ','.join(target_currency_list)

        response = self.request()
        return response

    def mapper(self):
        return self.result
