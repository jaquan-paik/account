from unittest.mock import patch

import jwt
from Crypto.PublicKey import RSA
from django.test import TestCase

from lib.ridibooks.internal_server_auth.helpers.config import ConfigHelper
from lib.ridibooks.internal_server_auth.helpers.jwt_auth import JwtAuthHelper

private = RSA.generate(bits=2048)
public = private.publickey()

dummy_config = ConfigHelper.generate_auth_data([
    {'iss': 'account', 'sub': 'library', 'secret': public.exportKey(), 'alg': 'RS256'},
    {'iss': 'account', 'sub': 'auth', 'secret': 'secret-hs256', 'alg': 'HS256'}
])


@patch('lib.ridibooks.internal_server_auth.config.RIDI_INTERNAL_AUTH_DATA', dummy_config)
class JwtAuthHelperTestCase(TestCase):
    def test_verify_with_invalid_rsa_token(self):
        invalid_rsa_token_by_invalid_iss = jwt.encode(
            key=private.exportKey(), payload={'iss': 'platform', 'sub': 'library'}, algorithm='RS256'
        ).decode('utf-8')
        invalid_rsa_token_by_invalid_sub = jwt.encode(
            key=private.exportKey(), payload={'iss': 'account', 'sub': 'book'}, algorithm='RS256'
        ).decode('utf-8')

        self.assertFalse(JwtAuthHelper.verify(token=invalid_rsa_token_by_invalid_iss))
        self.assertFalse(JwtAuthHelper.verify(token=invalid_rsa_token_by_invalid_sub))

    def test_verify_with_invalid_hs_token(self):
        invali_hs_token_by_invalid_iss = jwt.encode(key='secret-hs256', payload={'iss': 'platform', 'sub': 'library'}).decode('utf-8')
        invali_hs_token_by_invalid_sub = jwt.encode(key='secret-hs256', payload={'iss': 'account', 'sub': 'book'}).decode('utf-8')

        self.assertFalse(JwtAuthHelper.verify(token=invali_hs_token_by_invalid_iss))
        self.assertFalse(JwtAuthHelper.verify(token=invali_hs_token_by_invalid_sub))

    def test_verify_with_valid_rsa_token(self):
        valid_rsa_token = jwt.encode(key=private.exportKey(), payload={'iss': 'account', 'sub': 'library'}, algorithm='RS256')\
            .decode('utf-8')

        self.assertTrue(JwtAuthHelper.verify(token=valid_rsa_token))

    def test_verify_with_valid_hs_token(self):
        valid_hs_token = jwt.encode(key='secret-hs256', payload={'iss': 'account', 'sub': 'auth'}).decode('utf-8')
        self.assertTrue(JwtAuthHelper.verify(token=valid_hs_token))
