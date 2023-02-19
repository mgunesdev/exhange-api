import json
from urllib.parse import urlencode

import requests


class BaseClient:
    api_key = None
    client = None
    url = None
    method = None
    headers = None
    payload = None

    def exchange_rate(self, source_currency, target_currency_list):
        pass

    def exchange(self, source_amount, source_currency, target_currency):
        pass

    def exchange_list(self, start_date=None, end_date=None, source_currency=None, target_currency_list=None):
        pass

    def request(self):
        self.url = self.url.format(self.method, urlencode(self.payload, safe=':+'))
        response = requests.request(
            "GET",
            self.url,
            headers=self.headers,
            data={}
        )
        if response.status_code == 200:
            return json.loads(response.text)
        return None
