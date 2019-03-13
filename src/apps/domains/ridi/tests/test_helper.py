import requests_mock
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G

from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.token_request_helper import TokenRequestHelper
from apps.domains.ridi.helpers.url_helper import UrlHelper
from apps.domains.oauth2.models import Application
from infra.configure.config import GeneralConfig


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

        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'https://ridibooks.com/account/oauth-authorize-callback?return_url=https%3A%2F%2Fridibooks.com%3Futm_source%3Dridibooks_app%26utm_medium%3Dandroid%26utm_campaign%3Dtabbar_home%26utm_term%3D8.10.2'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'https://account.ridibooks.com/ridi/complete'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'https://view.ridibooks.com/books/3049001683&scope=&response_type=code'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'https://ridibooks.com/account/oauth-authorize-callback?return_url=https%3A%2F%2Fselect.ridibooks.com%3Futm_source%3Dridibooks_app%26utm_medium%3Dandroid%26utm_campaign%3D%26utm_term%3D9.1.2'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'https://ezwel.ridibooks.com/account/myridi&scope=&state=754fd837efd08b35&response_type=code'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'https://ridibooks.com/account/oauth-authorize-callback?return_url=https%3A%2F%2Fridibooks.com%2Forder%2Fcheckout%2Fcash%3Fb_ids%255B0%255D%3D2057042251%26return_url%3Dhttps%253A%252F%252Fridibooks.com%252Fpayment%252Frequest%252Fcash-and-point-auto%253Fb_ids%25255B0%25255D%253D2057042251%2526pay_object%253Dbuy%2526_token%253DZJ_oz4IgBKkc-hRartd6GIstPAqd3V3foUf2EiTCZmDoYuocUsZ_WBQI-cCWgSLZh1IcRxpnfaMdTfAJ1sMqfw%26utm_source%3Dridibooks_app%26utm_medium%3Dandroid%26utm_campaign%3D%26utm_term%3D9.1.2'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'https://ridibooks.com/account/oauth-authorize-callback?return_url=https%3A%2F%2Fridibooks.com%2Flibrary%2F%3Futm_source%3DRidibooks_APP%26utm_medium%3Dandroid%26utm_campaign%3Dmyridi%26utm_term%3D9.1.2'))
        self.assertEqual(None, ClientHelper.assert_in_house_client_redirect_uri(self.client, 'app://authorized'))


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
