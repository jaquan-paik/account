from django.test import TestCase

from lib.base.exceptions import MsgException
from lib.settings.asserts import assert_allowed_hosts_with_cookie_root_domain


class SettingAssertTestCase(TestCase):
    def setUp(self):
        self.valid_hosts = ['account.dev.ridi.io', 'local.dev.ridi.io', 'test.ridi.io']
        self.invalid_hosts = ['account.dev.invalid.io', 'ridibooks.com']
        self.root_domain = '.ridi.io'

    def test_assert(self):
        self.assertEqual(assert_allowed_hosts_with_cookie_root_domain(self.valid_hosts, self.root_domain), None)

    def test_assert_invalid_hosts(self):
        with self.assertRaises(MsgException):
            assert_allowed_hosts_with_cookie_root_domain(self.invalid_hosts, self.root_domain)
