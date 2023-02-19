import logging
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from core.models import User

logger = logging.getLogger(__name__)


class ApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        token, created = Token.objects.get_or_create(user=self.user)
        self.headers = {'X-PROVIDER': '1'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_exchange_rates(self):
        logger.debug('Starting test exchange/rates')
        url = '/api/v1/exchange/rates/'
        data = {
            "source_currency": "EUR",
            "target_currency_list": [
                "GBP",
                "USD"
            ]
        }

        logger.debug('Sending TEST data to url: %s, data: %s' % (url, data))
        response = self.client.post(url, data, format='json')

        logger.debug('Testing status code response: %s, code: %d' % (response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing exchange/rates was successfully')

    def test_exchange_convert(self):
        logger.debug('Starting test exchange/convert')
        url = '/api/v1/exchange/convert/'
        data = {
            "source_amount": 5,
            "source_currency": "EUR",
            "target_currency_list": [
                "GBP",
                "USD"
            ]
        }

        logger.debug('Sending TEST data to url: %s, data: %s' % (url, data))
        response = self.client.post(url, data, format='json')

        logger.debug('Testing status code response: %s, code: %d' % (response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing exchange/convert was successfully')

    def test_exchange_list(self):
        logger.debug('Starting test exchange/list')
        url = '/api/v1/exchange/list/'
        data = {
            "start_date": "2023-02-18",
            "end_date": "2023-02-19",
            "source_currency": "EUR",
            "target_currency_list": [
                "GBP",
                "USD"
            ]
        }

        logger.debug('Sending TEST data to url: %s, data: %s' % (url, data))
        response = self.client.post(url, data, format='json')

        logger.debug('Testing status code response: %s, code: %d' % (response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing exchange/list was successfully')
