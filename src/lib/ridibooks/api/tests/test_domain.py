from unittest.mock import patch, MagicMock

from django.test import TestCase

from lib.ridibooks.api.domain import ApiDomain


class Dummy:
    domain = ApiDomain(dev='this-is-dev', prod='this-is-prod')


class ApiDomainTestCase(TestCase):
    def setUp(self):
        self.dummy = Dummy()

    @patch('infra.configure.config.GeneralConfig.is_dev', MagicMock(return_value=True))
    def test_domain_with_dev(self):
        self.assertEqual(self.dummy.domain, 'this-is-dev')

    @patch('infra.configure.config.GeneralConfig.is_dev', MagicMock(return_value=False))
    def test_domain_with_prod(self):
        self.assertEqual(self.dummy.domain, 'this-is-prod')
