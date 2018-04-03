from django.test import TestCase, RequestFactory
from django.urls import reverse

from apps.domains.callback.constants import CookieRootDomains
from apps.domains.callback.exceptions import NotAllowedRootDomainException
from apps.domains.callback.helpers.url_helper import UrlHelper
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
            _ = UrlHelper.get_root_domain(request)
