from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django_dynamic_fixture import G

from apps.domains.callback.dtos import OAuth2Data
from apps.domains.oauth2.models import Application


class OAuth2DataTestCase(TestCase):
    def setUp(self):
        self.in_house_client = G(Application, skip_authorization=True, user=None, is_in_house=True, redirect_uris='https://test.com')
        self.normal_client = G(Application, user=None, redirect_uris='https://test.com')

    def test_raise_when_create(self):
        with self.assertRaises(PermissionDenied):
            OAuth2Data(state='1234', client_id=None, redirect_uri='https://test.com')

        with self.assertRaises(PermissionDenied):
            OAuth2Data(state='1234', client_id=self.in_house_client.client_id, redirect_uri=None)

    def test_invalid(self):
        with self.assertRaises(PermissionDenied):
            OAuth2Data(client_id=self.normal_client.client_id, state=None, redirect_uri='https://test.com').validate_client()

        with self.assertRaises(PermissionDenied):
            OAuth2Data(client_id=self.in_house_client.client_id, state=None, redirect_uri='https://fake-test.com').validate_redirect_uri()

        with self.assertRaises(PermissionDenied):
            OAuth2Data(client_id=self.normal_client, state='1234', redirect_uri='https://test.com').validate_state('4321')

    def test_validate(self):
        oauth2_data = OAuth2Data(state='1234', client_id=self.in_house_client.client_id, redirect_uri='https://test.com')

        try:
            oauth2_data.validate_client()
            oauth2_data.validate_redirect_uri()
            oauth2_data.validate_state(state='1234')
        except PermissionDenied:
            self.fail('OAuth2Data Validate Fail')

    def test_validate_when_state_is_none(self):
        oauth2_data = OAuth2Data(state=None, client_id=self.in_house_client.client_id, redirect_uri='https://test.com')

        try:
            oauth2_data.validate_state(state=None)
        except PermissionDenied:
            self.fail('OAuth2Data Validate Fail')

        with self.assertRaises(PermissionDenied):
            oauth2_data.validate_state(state='1234')
