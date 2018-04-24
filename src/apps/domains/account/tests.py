import requests_mock
from django.http import SimpleCookie
from django.test import Client, TestCase
from django.urls import reverse

from infra.configure.config import GeneralConfig
from lib.ridibooks.php_auth.api_url import RidiStoreApiUrl


class RidiLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_COOKIE=SimpleCookie({'PHPSESSID': 1111}).output(header='', sep='; '))

    def test_redirect(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(GeneralConfig.get_ridibooks_login_url(), response.url)

    def test_login_success(self):
        with requests_mock.mock() as m:
            m.get(RidiStoreApiUrl.get_url(RidiStoreApiUrl.ACCOUNT_INFO), json={'result': {'idx': 1111, 'id': 'testuser'}})

            response = self.client.get(reverse('account:login'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/accounts/profile/')
