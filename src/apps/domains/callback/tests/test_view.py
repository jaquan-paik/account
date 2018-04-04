from django.test import TestCase, Client
from django.urls import reverse

from infra.configure.config import GeneralConfig


class InHouseCallbackTestCase(TestCase):
    """
    AuthorizeView 와 CallbackView를 함께 테스트한다.
    """
    pass


class TokenViewTestCase(TestCase):
    pass


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout(self):
        response = self.client.get(reverse('ridi:logout') + '?return_url=https://test.com', HTTP_HOST=GeneralConfig.get_site_domain())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://test.com')
