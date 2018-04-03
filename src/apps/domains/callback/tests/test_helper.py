from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django_dynamic_fixture import G

from apps.domains.callback.constants import CookieRootDomains
from apps.domains.callback.exceptions import NotAllowedRootDomainException
from apps.domains.callback.helpers.client_helper import ClientHelper
from apps.domains.callback.helpers.url_helper import UrlHelper
from apps.domains.oauth2.models import Application
from infra.configure.config import GeneralConfig


class UrlHelperTestCase(TestCase):
    def test_redirect_uri(self):
        redirect_uri = UrlHelper.get_redirect_uri()

        self.assertIn('https://', redirect_uri)
        self.assertIn(GeneralConfig.get_site_domain(), redirect_uri)
        self.assertIn(reverse("ridi:callback"), redirect_uri)

    def test_get_token(self):
        token_url = UrlHelper.get_token()

        self.assertIn('https://', token_url)
        self.assertIn(GeneralConfig.get_site_domain(), token_url)
        self.assertIn(reverse("oauth2_provider:token"), token_url)

    def test_get_root_domain(self):
        factory = RequestFactory()
        request = factory.get('/', HTTP_HOST=GeneralConfig.get_site_domain())

        self.assertEqual(UrlHelper.get_root_domain(request=request), CookieRootDomains.to_string(CookieRootDomains.PROD_RIDI_COM))

    def test_raise_not_allow_host(self):
        factory = RequestFactory()
        request = factory.get('/', HTTP_HOST='dev.ridi.com')

        with self.assertRaises(NotAllowedRootDomainException):
            UrlHelper.get_root_domain(request)


class ClientHelperTestCase(TestCase):
    def setUp(self):
        self.client = G(Application, skip_authorization=True, user=None)
        self.not_implement_client = G(Application, skip_authorization=True, user=None, authorization_grant_type="implicit")

    def test_get_client(self):
        client = ClientHelper.get_client(client_id=self.client.client_id)
        self.assertEqual(client.client_id, self.client.client_id)

    def test_not_exists_client(self):
        with self.assertRaises(ObjectDoesNotExist):
            ClientHelper.get_client(client_id='is_dummy')

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            ClientHelper.get_client(client_id=self.not_implement_client.client_id)
