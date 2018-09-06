from django.test import TestCase

from lib.ridibooks.internal_server_auth.constants import AuthList, DEFAULT_ALG
from lib.ridibooks.internal_server_auth.helpers.config_helper import ConfigHelper


class ConfigHelperTestCase(TestCase):
    def test_generate_success(self):
        data_list = {
            AuthList.USER_BOOK_TO_LIBRARY: 'secret-one',
            AuthList.LIBRARY_TO_BOOK: 'secret-two',
        }

        config = ConfigHelper.generate_auth_data(data_list)

        self.assertEqual(config[AuthList.USER_BOOK_TO_LIBRARY].audience, 'library')
        self.assertEqual(config[AuthList.USER_BOOK_TO_LIBRARY].issuer, 'user-book')
        self.assertEqual(config[AuthList.USER_BOOK_TO_LIBRARY].secret, 'secret-one')
        self.assertEqual(config[AuthList.USER_BOOK_TO_LIBRARY].alg, DEFAULT_ALG)

        self.assertEqual(config[AuthList.LIBRARY_TO_BOOK].audience, 'book')
        self.assertEqual(config[AuthList.LIBRARY_TO_BOOK].issuer, 'library')
        self.assertEqual(config[AuthList.LIBRARY_TO_BOOK].secret, 'secret-two')
        self.assertEqual(config[AuthList.LIBRARY_TO_BOOK].alg, DEFAULT_ALG)
