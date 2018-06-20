# pylint: disable=protected-access

from unittest import TestCase

import requests
import requests_mock

from lib.ridibooks.api.base import BaseApi
from lib.ridibooks.common.constants import HttpMethod
from lib.ridibooks.common.exceptions import HTTPException, ServerException


class DummyApi(BaseApi):
    domain = 'https://dummy.com'

    TEST_API = '/test/api/'

    def get_test_domain(self):
        return self._request(method=HttpMethod.GET, path=self.TEST_API)


class ApiTestCase(TestCase):
    def setUp(self):
        self.dummy_api = DummyApi(access_token='dummy-access-token')

    def test_make_url(self):
        self.assertEqual(self.dummy_api._make_url(self.dummy_api.TEST_API), 'https://dummy.com/test/api/')

    def test_make_cookie(self):
        self.assertIn('ridi-at', self.dummy_api._make_cookies())
        self.assertEqual(self.dummy_api._make_cookies()['ridi-at'], 'dummy-access-token')

    def test_get_test_domain_200(self):
        with requests_mock.mock() as m:
            m.get(self.dummy_api._make_url(self.dummy_api.TEST_API), json={
                'message': 'success'
            })

            data = self.dummy_api.get_test_domain()
            self.assertEqual(data['message'], 'success')

    def test_get_test_domain_401(self):
        with self.assertRaises(HTTPException) as context:
            with requests_mock.mock() as m:
                m.get(self.dummy_api._make_url(self.dummy_api.TEST_API), text='401 Unauthorized', status_code=401)

                self.dummy_api.get_test_domain()

        exception = context.exception
        self.assertEqual(exception.status, 401)
        self.assertEqual(exception.content, b'401 Unauthorized')

    def test_get_test_domain_server_error(self):
        with self.assertRaises(ServerException):
            with requests_mock.mock() as m:
                m.get(self.dummy_api._make_url(self.dummy_api.TEST_API), exc=requests.exceptions.HTTPError)

                self.dummy_api.get_test_domain()
