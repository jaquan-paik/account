from django.http import HttpResponse
from django.test import TestCase

from apps.domains.ridi.dtos import TokenData
from apps.domains.ridi.helpers.response_cookie_helper import ResponseCookieHelper
from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY


class TokenCookieMixinTestCase(TestCase):
    def setUp(self):
        self.at = TokenData('access-token', 11111111)
        self.rt = TokenData('refresh-token', 12345678)

        self.helper = ResponseCookieHelper()

    def test_set_and_clear_cookie(self):
        response = HttpResponse()

        self.helper.add_token_cookie(response=response, access_token=self.at, refresh_token=self.rt)
        self.assertIn(ACCESS_TOKEN_COOKIE_KEY, response.cookies)
        self.assertIn(REFRESH_TOKEN_COOKIE_KEY, response.cookies)
        self.assertEqual(self.at.expires_in, response.cookies[ACCESS_TOKEN_COOKIE_KEY]['max-age'])
        self.assertEqual(self.rt.expires_in, response.cookies[REFRESH_TOKEN_COOKIE_KEY]['max-age'])

        self.helper.clear_token_cookie(response=response)
        self.assertEqual(0, response.cookies[ACCESS_TOKEN_COOKIE_KEY]['max-age'])
        self.assertEqual(0, response.cookies[REFRESH_TOKEN_COOKIE_KEY]['max-age'])

    def test_only_clear(self):
        response = HttpResponse()
        self.helper.clear_token_cookie(response=response)

        self.assertIn(ACCESS_TOKEN_COOKIE_KEY, response.cookies)
        self.assertIn(REFRESH_TOKEN_COOKIE_KEY, response.cookies)
        self.assertEqual(0, response.cookies[ACCESS_TOKEN_COOKIE_KEY]['max-age'])
        self.assertEqual(0, response.cookies[REFRESH_TOKEN_COOKIE_KEY]['max-age'])
