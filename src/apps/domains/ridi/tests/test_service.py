import requests_mock
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django_dynamic_fixture import G

from apps.domains.account.models import User
from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.url_helper import UrlHelper
from apps.domains.ridi.services.token_refresh_service import TokenRefreshService
from apps.domains.oauth2.models import Application, RefreshToken


class TokenRefreshServiceTestCase(TestCase):
    def setUp(self):
        user = G(User)

        in_house_client = G(Application, skip_authorization=True, user=None, is_in_house=True)
        self.refresh_token = G(
            RefreshToken, application=in_house_client, user=user, scope='all', token='this-is-refresh-token',
            access_token=None
        )

        not_in_house_client = G(Application, skip_authorization=True, user=None, is_in_house=False)
        self.not_in_house_refresh_token = G(
            RefreshToken, application=not_in_house_client, user=user, scope='all', token='this-is-not-in-house-token',
            access_token=None
        )

    def test_not_exist_refresh_token(self):
        token = 'this is invalid token'
        with self.assertRaises(PermissionDenied):
            TokenRefreshService.get_tokens(token)

    def test_not_in_house_client(self):
        with self.assertRaises(PermissionDenied):
            TokenRefreshService.get_tokens(self.not_in_house_refresh_token.token)

    def test_success_refresh(self):
        with requests_mock.mock() as m:
            m.post(UrlHelper.get_oauth2_token_url(), json={
                'access_token': 'test-access-token2222',
                'expires_in': 1111111,
                'refresh_token': 'test-refresh-token2222',
                'refresh_token_expires_in': 2222222,
            })

            at, rt = TokenRefreshService.get_tokens(self.refresh_token.token)
            self.assertIsInstance(at, TokenData)
            self.assertIsInstance(rt, TokenData)

            self.assertEqual(at.token, 'test-access-token2222')
            self.assertEqual(at.expires_in, 1111111)
            self.assertEqual(rt.token, 'test-refresh-token2222')
            self.assertEqual(rt.expires_in, 2222222)
