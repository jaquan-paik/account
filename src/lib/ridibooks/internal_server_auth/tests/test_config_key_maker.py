from django.test import TestCase

from lib.ridibooks.internal_server_auth.utils import ConfigKeyMaker


class MakeAuthDataKeyTestCase(TestCase):
    def test_make_res_key(self):
        issuer = 'account'
        audience = 'library'

        key = ConfigKeyMaker.make_res_key(issuer, audience)
        self.assertEqual(key, f'{issuer}:{audience}')

    def test_make_req_key(self):
        issuer = 'library'
        audience = 'account'

        key = ConfigKeyMaker.make_req_key(issuer, audience)
        self.assertEqual(key, f'{issuer}:{audience}')
