import requests_mock
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django_dynamic_fixture import G

from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.exceptions import NotAllowedRootDomainException
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

    def test_get_root_domain(self):
        factory = RequestFactory()
        request = factory.get('/', HTTP_HOST=GeneralConfig.get_site_domain())

        self.assertIn(
            UrlHelper.get_allowed_cookie_root_domain(request=request), settings.ALLOWED_COOKIE_ROOT_DOMAINS
        )

    def test_raise_not_allow_host(self):
        factory = RequestFactory()
        request = factory.get('/', HTTP_HOST='dev.ridi.com')

        with self.assertRaises(NotAllowedRootDomainException):
            UrlHelper.get_allowed_cookie_root_domain(request)


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
