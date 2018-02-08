from unittest.mock import MagicMock

from django.test import TestCase

from lib.email.exceptions import EmailErrorException
from .services import email_blacklist_service, email_service


class EmailValidationTestCase(TestCase):
    def setUp(self):
        self.emoji_included_email = '😞@email.com'
        self.no_dot_email = 'invalid@email'
        self.no_at_email = 'invalid.com'
        self.blacklist_email = 'blacklist@email.com'

        def is_blacklist_email(email: str) -> bool:
            return email == self.blacklist_email

        email_blacklist_service.is_in_blacklist = MagicMock(side_effect=is_blacklist_email)

    def test_email_validation(self):
        with self.assertRaises(EmailErrorException):
            email_service.assert_if_not_valid_email(self.emoji_included_email)

        with self.assertRaises(EmailErrorException):
            email_service.assert_if_not_valid_email(self.no_dot_email)

        with self.assertRaises(EmailErrorException):
            email_service.assert_if_not_valid_email(self.no_at_email)

        with self.assertRaises(EmailErrorException):
            email_service.assert_if_not_valid_email(self.blacklist_email)
