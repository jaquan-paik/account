# pylint: disable=line-too-long
# flake8: noqa
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBase
from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G

from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper, COOKIE_EXPIRE_DEFAULT_TIME
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
        self.client = G(
            Application, skip_authorization=True, user=None, is_in_house=True,
            _redirect_uris='https://view.ridibooks.com/books/ https://account.ridibooks.com/ridi/callback/ app://authorized https://ridibooks.com/ https://select.ridibooks.com https://ezwel.ridibooks.com https://pay.ridibooks.com https://library.ridibooks.com/'
        )
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

    def test_assert_redirect_uris(self):
        with self.assertRaises(PermissionDenied):
            ClientHelper.assert_in_house_client_redirect_uri(self.client, 'https://ridi.io/ridi/complete')
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client,
                                                                                'https://ridibooks.com/account/oauth-authorize-callback?return_url=https%3A%2F%2Fridibooks.com%3Futm_source%3Dridibooks_app%26utm_medium%3Dandroid%26utm_campaign%3Dtabbar_home%26utm_term%3D8.10.2'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'https://account.ridibooks.com/ridi/complete'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client,
                                                                                'https://view.ridibooks.com/books/3049001683&scope=&response_type=code'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client,
                                                                                'https://ridibooks.com/account/oauth-authorize-callback?return_url=https%3A%2F%2Fselect.ridibooks.com%3Futm_source%3Dridibooks_app%26utm_medium%3Dandroid%26utm_campaign%3D%26utm_term%3D9.1.2'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client,
                                                                                'https://ezwel.ridibooks.com/account/myridi&scope=&state=754fd837efd08b35&response_type=code'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client,
                                                                                'https://ridibooks.com/account/oauth-authorize-callback?return_url=https%3A%2F%2Fridibooks.com%2Forder%2Fcheckout%2Fcash%3Fb_ids%255B0%255D%3D2057042251%26return_url%3Dhttps%253A%252F%252Fridibooks.com%252Fpayment%252Frequest%252Fcash-and-point-auto%253Fb_ids%25255B0%25255D%253D2057042251%2526pay_object%253Dbuy%2526_token%253DZJ_oz4IgBKkc-hRartd6GIstPAqd3V3foUf2EiTCZmDoYuocUsZ_WBQI-cCWgSLZh1IcRxpnfaMdTfAJ1sMqfw%26utm_source%3Dridibooks_app%26utm_medium%3Dandroid%26utm_campaign%3D%26utm_term%3D9.1.2'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client,
                                                                                'https://ridibooks.com/account/oauth-authorize-callback?return_url=https%3A%2F%2Fridibooks.com%2Flibrary%2F%3Futm_source%3DRidibooks_APP%26utm_medium%3Dandroid%26utm_campaign%3Dmyridi%26utm_term%3D9.1.2'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'app://authorized'))


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
