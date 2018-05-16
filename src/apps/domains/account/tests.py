# pylint: disable=protected-access
import requests_mock
from django.http import SimpleCookie
from django.test import Client, TestCase
from django.urls import reverse

from infra.configure.config import GeneralConfig
from lib.ridibooks.api.store import StoreApi


class RidiLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_COOKIE=SimpleCookie({'PHPSESSID': 1111}).output(header='', sep='; '))
        self.api = StoreApi()

    def test_redirect(self):
        response = self.client.get(reverse('account:login'), secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertIn(GeneralConfig.get_ridibooks_login_url(), response.url)

    def test_login_success(self):
        with requests_mock.mock() as m:
            m.get(self.api._make_url(StoreApi.ACCOUNT_INFO), json={'result': {'idx': 1, 'id': 'testuser'}})

            response = self.client.get(reverse('account:login'), secure=True)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/')
