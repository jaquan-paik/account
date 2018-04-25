from django.http import HttpResponseForbidden
from django.test import RequestFactory, TestCase
from lib.ridibooks.ip.middlewares import RidiIPFilterMiddleware

from lib.ridibooks.ip.constants import RidiIP


class RidiMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RidiIPFilterMiddleware()

    def test_process_request(self):
        local_request = self.factory.get('', REMOTE_ADDR='127.0.0.1')
        ridi_request = self.factory.get('', REMOTE_ADDR=RidiIP.OFFICE_01)
        external_request = self.factory.get('', REMOTE_ADDR='13.124.60.0')

        self.assertIsNone(self.middleware.process_request(request=local_request))
        self.assertIsNone(self.middleware.process_request(request=ridi_request))
        self.assertIsInstance(self.middleware.process_request(request=external_request), HttpResponseForbidden)
