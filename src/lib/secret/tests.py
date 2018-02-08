import json
from unittest.mock import MagicMock

from django.test import TestCase

from lib.secret.secret import SecretFileHandler, _Secret


class SecretTestCase(TestCase):
    def setUp(self):
        self.dummyConfig = {
            'name': 'jungle',
            'gender': 'male',
            'hobby': 'boardgame',
            'testtest': 'thisistest',
        }
        self.dummyVersion = 'v1'
        SecretFileHandler.load = MagicMock(return_value=json.dumps(self.dummyConfig))
        _Secret._load_version_file = MagicMock(return_value=self.dummyVersion)  # flake8: noqa: W0212  # pylint:disable=protected-access

        self.secret = _Secret()

    def test_load_config(self):
        self.assertEqual(self.secret.get('name'), self.dummyConfig['name'])
        self.assertEqual(self.secret.get('gender'), self.dummyConfig['gender'])
        self.assertEqual(self.secret.get('hobby'), self.dummyConfig['hobby'])
        self.assertEqual(self.secret.get('testtest'), self.dummyConfig['testtest'])

    def test_load_version(self):
        self.assertEqual(self.secret.version, self.dummyVersion)
