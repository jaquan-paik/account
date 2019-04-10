from django.test import TestCase
from typing import Dict
from unittest.mock import MagicMock

from lib.aws.parameter_store import ParameterStoreConnector
from lib.secret.constants import SecretEnvironment


class ParameterStoreConnectorTestCase(TestCase):
    def test_parse_parameters(self):
        ParameterStoreConnector.__init__ = MagicMock(return_value=None)
        connector = ParameterStoreConnector()

        for env in map(SecretEnvironment.to_string, SecretEnvironment.get_list()):
            key_num = 4
            connector.load_parameters_by_path = MagicMock(return_value=self._dummy_parameter_response(env, key_num))
            params = connector.load_parameters(env)

            for n in range(0, key_num):
                self.assertEqual(params['test_key%s' % n], 'test_value%s' % n)

    def _dummy_parameter_response(self, env: str, key_num: int) -> Dict:

        return {
            'Parameters': [self._dummy_parameter('/%s/' % env, n) for n in range(0, key_num)]
        }

    def _dummy_parameter(self, path: str, n: int) -> Dict:
        return {
            'Name': '%stest_key%s' % (path, n),
            'Type': 'SecureString',
            'Value': 'test_value%s' % n,
            'Version': 1
        }
