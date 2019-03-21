# pylint: disable=protected-access
from datetime import datetime

import jwt
import requests_mock
from django.conf import settings
from django.http import SimpleCookie
from django.test import Client, TestCase
from django.urls import reverse

from apps.domains.oauth2.constants import JwtAlg
from infra.configure.config import GeneralConfig
from lib.ridibooks.api.store import StoreApi
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY


class RidiLoginViewTestCase(TestCase):
    def generate_access_token(self):
        payload = {
            'sub': 'testuser',
            'u_idx': 1,
            'exp': round(datetime.now().timestamp()) + 3600,
            'client_id': settings.RIDI_OAUTH2_CLIENT_ID,
            'scope': 'ALL'
        }

        return jwt.encode(payload, settings.RIDI_OAUTH2_JWT_SECRET, algorithm=JwtAlg.HS256).decode()

    def test_redirect(self):
        cookies = {'PHPSESSID': 1111}
        client = Client(HTTP_COOKIE=SimpleCookie(cookies).output(header='', sep='; '))

        response = client.get(reverse('account:login'), secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertIn(GeneralConfig.get_ridibooks_login_url(), response.url)

    def test_login_success(self):
        cookies = {'PHPSESSID': 1111, ACCESS_TOKEN_COOKIE_KEY: self.generate_access_token()}
        client = Client(HTTP_COOKIE=SimpleCookie(cookies).output(header='', sep='; '))
        api = StoreApi()

        with requests_mock.mock() as m:
            m.get(api._make_url(StoreApi.ACCOUNT_INFO), json={'result': {'idx': 1, 'id': 'testuser'}})

            response = client.get(reverse('account:login'), secure=True)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/')
