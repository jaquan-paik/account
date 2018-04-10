from django.test import TestCase
from django_dynamic_fixture import G

from apps.domains.account.models import User
from apps.domains.oauth2.constants import JwtAlg
from apps.domains.oauth2.models import Application
from apps.domains.oauth2.token import JwtHandler


class JwtHandlerTestCase(TestCase):
    def setUp(self):
        self.user = G(User, idx=1, id='testuser')
        self.valid_client = G(Application, skip_authorization=True, user=None)
        self.invalid_client = G(Application, skip_authorization=True, user=None, jwt_alg=JwtAlg.RS256)

    def test_generate_with_invalid_client(self):
        class req:
            user = self.user
            client = self.invalid_client
            scopes = ['all']

        with self.assertRaises(NotImplementedError):
            JwtHandler.generate(req)

    def test_generate_with_valid_client(self):
        class req:
            user = self.user
            client = self.valid_client
            scopes = ['all']

        try:
            JwtHandler.generate(req)
        except NotImplementedError:
            self.fail('Jwt Generate Test Fail')

    def test_get_access_token(self):
        class req:
            user = self.user
            client = self.valid_client
            scopes = ['all']

        jwt_token = JwtHandler.generate(req)
        access_token = JwtHandler.get_access_token(token=jwt_token)

        self.assertEqual(access_token.token, jwt_token)
        self.assertEqual(access_token.user, self.user)
        self.assertEqual(access_token.application, self.valid_client)
        self.assertEqual(access_token.scope, 'all')
