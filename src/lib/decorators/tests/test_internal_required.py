from unittest.mock import MagicMock

from django.http import HttpResponse, HttpResponseForbidden
from django.test import RequestFactory, TestCase

from lib.decorators.internal_required import internal_required


class InternalRequiredTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = internal_required(MagicMock(return_value=HttpResponse('hello world')))

    def test_internal_ip(self):
        request = self.factory.get('', REMOTE_ADDR='127.0.0.1')
        response = self.view(request=request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'hello world')

    def test_external_ip(self):
        request = self.factory.get('', REMOTE_ADDR='13.124.60.0')
        response = self.view(request=request)

        self.assertIsInstance(response, HttpResponseForbidden)
