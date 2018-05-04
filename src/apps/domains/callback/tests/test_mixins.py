from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django_dynamic_fixture import G

from apps.domains.callback.dtos import TokenData
from apps.domains.callback.mixins import OAuth2SessionMixin, SESSION_CLIENT_ID_KEY, SESSION_REDIRECT_URI_KEY, SESSION_STATE_KEY, \
    TokenCookieMixin
from apps.domains.oauth2.models import Application
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY


class TokenCookieMixinTestCase(TestCase):
    def setUp(self):
        self.at = TokenData('access-token', 11111111)
        self.rt = TokenData('refresh-token', 12345678)

        self.mixin = TokenCookieMixin()

    def test_set_and_clear_cookie(self):
        response = HttpResponse()

        self.mixin.add_token_cookie(response=response, access_token=self.at, refresh_token=self.rt, root_domain='test.com')
        self.assertIn(ACCESS_TOKEN_COOKIE_KEY, response.cookies)
        self.assertIn(REFRESH_TOKEN_COOKIE_KEY, response.cookies)
        self.assertEqual(self.at.expires_in, response.cookies[ACCESS_TOKEN_COOKIE_KEY]['max-age'])
        self.assertEqual(self.rt.expires_in, response.cookies[REFRESH_TOKEN_COOKIE_KEY]['max-age'])

        self.mixin.clear_token_cookie(response=response, root_domain='test.com')
        self.assertEqual(0, response.cookies[ACCESS_TOKEN_COOKIE_KEY]['max-age'])
        self.assertEqual(0, response.cookies[REFRESH_TOKEN_COOKIE_KEY]['max-age'])

    def test_only_clear(self):
        response = HttpResponse()
        self.mixin.clear_token_cookie(response=response, root_domain='test.com')

        self.assertIn(ACCESS_TOKEN_COOKIE_KEY, response.cookies)
        self.assertIn(REFRESH_TOKEN_COOKIE_KEY, response.cookies)
        self.assertEqual(0, response.cookies[ACCESS_TOKEN_COOKIE_KEY]['max-age'])
        self.assertEqual(0, response.cookies[REFRESH_TOKEN_COOKIE_KEY]['max-age'])


class OAuth2SessionMixinTestCase(TestCase):
    def setUp(self):
        factory = RequestFactory()
        self.mixin = OAuth2SessionMixin()
        self.mixin.request = factory.get('/')
        self.mixin.request.session = {}

        self.client = G(Application, skip_authorization=True, user=None, is_in_house=True, redirect_uris='https://test.com')

    def test_set_oauth2_data(self):
        self.mixin.set_oauth2_data(client_id=self.client.client_id, redirect_uri='https://test.com', state='1234')

        self.assertIn(SESSION_CLIENT_ID_KEY, self.mixin.request.session)
        self.assertIn(SESSION_REDIRECT_URI_KEY, self.mixin.request.session)
        self.assertIn(SESSION_STATE_KEY, self.mixin.request.session)

        self.assertEqual(self.mixin.get_session(SESSION_CLIENT_ID_KEY), self.client.client_id)
        self.assertEqual(self.mixin.get_session(SESSION_REDIRECT_URI_KEY), 'https://test.com')
        self.assertEqual(self.mixin.get_session(SESSION_STATE_KEY), '1234')

    def test_get_oauth2_data(self):
        self.mixin.set_oauth2_data(client_id=self.client.client_id, redirect_uri='https://test.com', state='1234')

        oauth2_data = self.mixin.get_oauth2_data(code='this-is-code', state='1234')

        self.assertEqual(oauth2_data.code, 'this-is-code')
        self.assertEqual(oauth2_data.client_id, self.client.client_id)
        self.assertEqual(oauth2_data.redirect_uri, 'https://test.com')
        self.assertEqual(oauth2_data.state, '1234')
