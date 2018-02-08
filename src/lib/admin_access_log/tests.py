from django.test import TestCase

from .constants import RequestMethod
from .models import AdminUrlAccessHistory
from .services import add_log


class RequestMethodTestCase(TestCase):
    def test_method_convert(self):
        with self.assertRaises(NotImplementedError):
            RequestMethod.convert('redirect')
        with self.assertRaises(AttributeError):
            RequestMethod.convert(1)

        self.assertEqual(RequestMethod.convert('GET'), RequestMethod.GET)
        self.assertEqual(RequestMethod.convert('gET'), RequestMethod.GET)
        self.assertEqual(RequestMethod.convert('Get'), RequestMethod.GET)
        self.assertEqual(RequestMethod.convert('get'), RequestMethod.GET)

        self.assertEqual(RequestMethod.convert('GET'), RequestMethod.GET)
        self.assertEqual(RequestMethod.convert('POST'), RequestMethod.POST)
        self.assertEqual(RequestMethod.convert('PUT'), RequestMethod.PUT)
        self.assertEqual(RequestMethod.convert('DELETE'), RequestMethod.DELETE)


class AdminUrlAccessHistoryTestCase(TestCase):
    def test_create(self):
        history = AdminUrlAccessHistory.create(2, RequestMethod.PUT, '/hello')
        self.assertEqual(history.staff_id, 2)
        self.assertEqual(history.method, RequestMethod.PUT)
        self.assertEqual(history.url, '/hello')

    def test_add_log(self):
        self.assertTrue(add_log(2, 'GET', '/hello'))
        self.assertFalse(add_log(2, 'GET', '/jsi18n/'))
