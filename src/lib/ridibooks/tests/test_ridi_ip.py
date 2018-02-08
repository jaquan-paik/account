from django.test import TestCase

from lib.ridibooks.ridi_ip import RidiIP


class RidiIpTestCase(TestCase):
    def test_is_ridi_ip(self):
        self.assertTrue(RidiIP.is_ridi_ip(RidiIP.OFFICE_01))
        self.assertTrue(RidiIP.is_ridi_ip(RidiIP.OFFICE_04))
        self.assertTrue(RidiIP.is_ridi_ip(RidiIP.VPN_01))
        self.assertTrue(RidiIP.is_ridi_ip(RidiIP.VPN_02))
        self.assertTrue(RidiIP.is_ridi_ip(RidiIP.IDC_01))

    def test_not_ridi_ip(self):
        self.assertFalse(RidiIP.is_ridi_ip('127.0.0.1'))
        self.assertFalse(RidiIP.is_ridi_ip('13.124.60.0'))
