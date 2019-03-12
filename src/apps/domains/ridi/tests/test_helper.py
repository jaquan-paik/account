import requests_mock
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBase
from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G

from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper, COOKIE_EXPIRE_DEFAULT_TIME
from apps.domains.ridi.helpers.token_request_helper import TokenRequestHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper
from apps.domains.oauth2.models import Application
from infra.configure.config import GeneralConfig

from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY


class UrlHelperTestCase(TestCase):
    def test_redirect_uri(self):
        redirect_uri = UrlHelper.get_callback_view_url()

        self.assertIn('https://', redirect_uri)
        self.assertIn(GeneralConfig.get_site_domain(), redirect_uri)
        self.assertIn(reverse("ridi:callback"), redirect_uri)

    def test_get_token(self):
        token_url = UrlHelper.get_oauth2_token_url()

        self.assertIn('https://', token_url)
        self.assertIn(GeneralConfig.get_site_domain(), token_url)
        self.assertIn(reverse("oauth2_provider:token"), token_url)


class ClientHelperTestCase(TestCase):
    def setUp(self):
        self.client = G(Application, skip_authorization=True, user=None)
        self.not_implement_client = G(Application, skip_authorization=True, user=None, authorization_grant_type="implicit")

    def test_get_client(self):
        client = ClientHelper.get_client(client_id=self.client.client_id)
        self.assertEqual(client.client_id, self.client.client_id)

    def test_not_exists_client(self):
        with self.assertRaises(PermissionDenied):
            ClientHelper.get_client(client_id='is_dummy')

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            ClientHelper.get_client(client_id=self.not_implement_client.client_id)


class TokenHelperTestCase(TestCase):
    def setUp(self):
        self.client = G(Application, skip_authorization=True, user=None)

    def test_token_code_helper(self):
        with requests_mock.mock() as m:
            m.post(UrlHelper.get_oauth2_token_url(), json={
                'access_token': 'test-access-token1111',
                'expires_in': 1111111,
                'refresh_token': 'test-refresh-token1111',
                'refresh_token_expires_in': 2222222,
            })
            at, rt = TokenRequestHelper.get_tokens(grant_type='authorization_code', client=self.client, code='test-code')

            self.assertIsInstance(at, TokenData)
            self.assertIsInstance(rt, TokenData)

            self.assertEqual(at.token, 'test-access-token1111')
            self.assertEqual(at.expires_in, 1111111)
            self.assertEqual(rt.token, 'test-refresh-token1111')
            self.assertEqual(rt.expires_in, 2222222)

    def test_token_refresh_helper(self):
        with requests_mock.mock() as m:
            m.post(UrlHelper.get_oauth2_token_url(), json={
                'access_token': 'test-access-token2222',
                'expires_in': 1111111,
                'refresh_token': 'test-refresh-token2222',
                'refresh_token_expires_in': 2222222,
            })
            at, rt = TokenRequestHelper.get_tokens(grant_type='refresh_token', client=self.client, refresh_token='test-refresh-token')

            self.assertIsInstance(at, TokenData)
            self.assertIsInstance(rt, TokenData)

            self.assertEqual(at.token, 'test-access-token2222')
            self.assertEqual(at.expires_in, 1111111)
            self.assertEqual(rt.token, 'test-refresh-token2222')
            self.assertEqual(rt.expires_in, 2222222)


class ResponseCookieHelperTestCase(TestCase):
    def setUp(self):
        self.access_token = TokenData(token='access_token', expires_in=3600)
        self.refresh_token = TokenData(token='refresh_token', expires_in=3600)

    def test_add_token_cookies_with_auto_login(self):
        response = HttpResponseBase()
        ResponseCookieHelper.add_token_cookie(response, self.access_token, self.refresh_token, True)

        self.assertIn(ACCESS_TOKEN_COOKIE_KEY, response.cookies)
        self.assertNotEqual(response.cookies[ACCESS_TOKEN_COOKIE_KEY]['expires'], COOKIE_EXPIRE_DEFAULT_TIME)
        self.assertEqual(response.cookies[ACCESS_TOKEN_COOKIE_KEY]['max-age'], self.access_token.expires_in)

        self.assertIn(REFRESH_TOKEN_COOKIE_KEY, response.cookies)
        self.assertNotEqual(response.cookies[REFRESH_TOKEN_COOKIE_KEY]['expires'], COOKIE_EXPIRE_DEFAULT_TIME)
        self.assertEqual(response.cookies[REFRESH_TOKEN_COOKIE_KEY]['max-age'], self.refresh_token.expires_in)

    def test_add_token_cookies_without_auto_login(self):
        response = HttpResponseBase()
        ResponseCookieHelper.add_token_cookie(response, self.access_token, self.refresh_token, False)

        self.assertIn(ACCESS_TOKEN_COOKIE_KEY, response.cookies)
        self.assertEqual(response.cookies[ACCESS_TOKEN_COOKIE_KEY]['expires'], '')
        self.assertEqual(response.cookies[ACCESS_TOKEN_COOKIE_KEY]['max-age'], '')

        self.assertIn(REFRESH_TOKEN_COOKIE_KEY, response.cookies)
        self.assertEqual(response.cookies[REFRESH_TOKEN_COOKIE_KEY]['expires'], '')
        self.assertEqual(response.cookies[REFRESH_TOKEN_COOKIE_KEY]['max-age'], '')

    def test_clear_token(self):
        response = HttpResponseBase()
        ResponseCookieHelper.add_token_cookie(response, self.access_token, self.refresh_token, False)

        ResponseCookieHelper.clear_token_cookie(response)
        self.assertEqual(response.cookies[ACCESS_TOKEN_COOKIE_KEY].value, '')
        self.assertEqual(response.cookies[ACCESS_TOKEN_COOKIE_KEY]['expires'], COOKIE_EXPIRE_DEFAULT_TIME)
        self.assertEqual(response.cookies[ACCESS_TOKEN_COOKIE_KEY]['max-age'], 0)

        self.assertEqual(response.cookies[REFRESH_TOKEN_COOKIE_KEY].value, '')
        self.assertEqual(response.cookies[REFRESH_TOKEN_COOKIE_KEY]['expires'], COOKIE_EXPIRE_DEFAULT_TIME)
        self.assertEqual(response.cookies[REFRESH_TOKEN_COOKIE_KEY]['max-age'], 0)
