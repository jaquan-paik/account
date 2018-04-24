from django.test import TestCase

from lib.ridibooks.auth.utils import make_auth_data_key


class MakeAuthDataKeyTestCase(TestCase):
    def test_make_key(self):
        issuer = 'account'
        subject = 'library'

        key = make_auth_data_key(issuer=issuer, subject=subject)
        self.assertEqual(key, f'{issuer}-{subject}')
