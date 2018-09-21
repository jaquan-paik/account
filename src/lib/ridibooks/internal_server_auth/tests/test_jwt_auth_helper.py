from unittest.mock import patch

import jwt
from Crypto.PublicKey import RSA
from django.test import TestCase

from lib.ridibooks.internal_server_auth.constants import AuthList
from lib.ridibooks.internal_server_auth.helpers.config_helper import ConfigHelper
from lib.ridibooks.internal_server_auth.helpers.internal_server_auth_helper import InternalServerAuthHelper

private1 = RSA.generate(bits=2048)
public1 = private1.publickey()

private2 = RSA.generate(bits=2048)
public2 = private2.publickey()

private3 = RSA.generate(bits=2048)
public3 = private3.publickey()

dummy_config = ConfigHelper.generate_auth_data({
    AuthList.USER_BOOK_TO_LIBRARY: public1.exportKey().decode(),
    AuthList.CPS_TO_LIBRARY: public2.exportKey().decode(),

    AuthList.LIBRARY_TO_BOOK: private3.exportKey().decode(),
})


@patch('lib.ridibooks.internal_server_auth.settings.RIDI_INTERNAL_AUTH_DATA', dummy_config)
class JwtAuthHelperTestCase(TestCase):
    def test_verify_with_invalid_rsa_token(self):
        invalid_rsa_token_by_invalid_iss = jwt.encode(
            key=private2.exportKey(), payload={'sub': 'command', 'aud': 'library'}, algorithm='RS256'
        ).decode('utf-8')
        invalid_rsa_token_by_invalid_sub = jwt.encode(
            key=private1.exportKey(), payload={'iss': 'user-book', 'sub': 'book-check'}, algorithm='RS256'
        ).decode('utf-8')

        self.assertFalse(InternalServerAuthHelper.verify(token=invalid_rsa_token_by_invalid_iss))
        self.assertFalse(InternalServerAuthHelper.verify(token=invalid_rsa_token_by_invalid_sub))

    def test_verify_with_valid_res_rsa_token(self):
        valid_rsa_token1 = jwt.encode(
            key=private2.exportKey(), payload={'iss': 'cps', 'sub': 'book-check', 'aud': 'library'}, algorithm='RS256'
        ).decode('utf-8')
        valid_rsa_token2 = jwt.encode(
            key=private1.exportKey(), payload={'iss': 'user-book', 'sub': 'command', 'aud': 'library'}, algorithm='RS256'
        ).decode('utf-8')

        self.assertTrue(InternalServerAuthHelper.verify(token=valid_rsa_token1))
        self.assertTrue(InternalServerAuthHelper.verify(token=valid_rsa_token2))

    def test_verify_with_valid_req_rsa_token(self):
        token = InternalServerAuthHelper.generate(AuthList.LIBRARY_TO_BOOK)
        payload = jwt.decode(jwt=token, key=public3.exportKey(), algorithms=['RS256'], audience='book')
        self.assertEqual(payload['iss'], 'library')
        self.assertEqual(payload['aud'], 'book')
