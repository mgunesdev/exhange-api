import datetime
import json

from decouple import config

from core.services.exchange.clients.base import BaseClient


class CurrencyDataClient(BaseClient):
    api_key = config('CURRENCY_DATA_API_KEY')
    url = "https://api.apilayer.com/currency_data/{}?{}"

    def __init__(self, payload=None):
        self.payload = payload
        self.headers = {
            "apikey": self.api_key
        }

    def exchange_rate(self, source_currency, target_currency_list):
        self.method = 'live'
        self.payload = {
            'source': source_currency,
            'currencies': ','.join(target_currency_list)
        }

        response = self.request()
        return self.mapper_for_exchange_rate(response, source_currency)

    def exchange(self, source_amount, source_currency, target_currency):
        self.method = 'convert'
        self.payload = {
            'to': source_currency,
            'from': target_currency,
            'amount': source_amount,
            'date': datetime.datetime.now().strftime("%Y-%m-%d")
        }

        return self.request()

    def exchange_list(self, start_date=None, end_date=None, source_currency=None, target_currency_list=None):
        self.method = 'timeframe'
        self.payload = {}

        if start_date:
            self.payload['start_date'] = start_date

        if end_date:
            self.payload['end_date'] = end_date

        if source_currency:
            self.payload['source'] = source_currency

        if target_currency_list:
            self.payload['currencies'] = ','.join(target_currency_list)

        response = self.request()

        return self.mapper_for_exchange_list(response, source_currency)

    def mapper_for_exchange_list(self, response, source_currency):
        if response and response['success']:
            rates = {}
            new_items = {}
            for key in response['quotes'].keys():
                items = response['quotes'][key]
                for item in items.keys():
                    new_key = item.replace(source_currency, '')
                    new_items[new_key] = response['quotes'][key][item]
                rates[key] = new_items
            response['rates'] = rates

        return response

    def mapper_for_exchange_rate(self, response, source_currency):
        if response and response['success']:
            rates = {}
            for key in response['quotes'].keys():
                new_key = key.replace(source_currency, '')
                rates[new_key] = response['quotes'][key]
            response['rates'] = rates

        return response
