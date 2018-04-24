from django.test import TestCase

from lib.ridibooks.auth.helpers.config import ConfigHelper


class ConfigHelperTestCase(TestCase):
    def test_generate_with_empty_array(self):
        empty_array = []
        config = ConfigHelper.generate_auth_data(empty_array)

        self.assertDictEqual(config, {})

    def test_generate_with_invalid_variable_type(self):
        with self.assertRaises(TypeError):
            ConfigHelper.generate_auth_data({})

        with self.assertRaises(TypeError):
            ConfigHelper.generate_auth_data("123123")

        with self.assertRaises(TypeError):
            ConfigHelper.generate_auth_data(1234)

    def test_generate_success(self):
        data_list = [
            {'iss': 'account', 'sub': 'library', 'secret': 'secret-one'},
            {'iss': 'account', 'sub': 'auth', 'secret': 'secret-two', 'alg': 'HS256'}
        ]

        config = ConfigHelper.generate_auth_data(data_list)

        self.assertEqual(config['account-library'], ('secret-one', 'RS256'))
        self.assertEqual(config['account-auth'], ('secret-two', 'HS256'))
