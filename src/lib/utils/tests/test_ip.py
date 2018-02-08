from django.test import RequestFactory, TestCase

from lib.utils.ip import get_client_ip_from_request, ip2long, is_internal_ip, is_ipv6, long2ip


class IpUtilTestCase(TestCase):
    def setUp(self):
        self.v4_loopback = '127.0.0.1'
        self.v6_loopback = '::1/128'

        self.v4_test_ip = '13.124.60.0'
        self.v6_test_ip = '2001:4A2B::1f3F'

        self.factory = RequestFactory()

    def test_ip_v6(self):
        self.assertFalse(is_ipv6(self.v4_loopback))
        self.assertTrue(is_ipv6(self.v6_loopback))
        self.assertFalse(is_ipv6(self.v4_test_ip))
        self.assertTrue(is_ipv6(self.v6_test_ip))

    def test_ip_convert_long(self):
        long_ip = ip2long(self.v4_loopback)
        ip = long2ip(long_ip)

        self.assertEqual(ip, self.v4_loopback)

    def test_get_ip_from_request(self):
        request = self.factory.get('')
        ip = get_client_ip_from_request(request)

        self.assertEqual(self.v4_loopback, ip)

    def test_internal_ip(self):
        self.assertTrue(is_internal_ip(self.v4_loopback))
        self.assertFalse(is_internal_ip(self.v4_test_ip))
