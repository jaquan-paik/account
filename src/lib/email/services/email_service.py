from typing import List

from email_validator import EmailNotValidError, validate_email

from infra.email.dto import Email
from infra.email.exceptions import EmailSendErrorException
from infra.email.helper import MailgunHelper, MandrillHelper
from lib.log import sentry
from lib.utils.string import is_include_emoji
from . import email_blacklist_service
from ..exceptions import EmailErrorException


def assert_if_not_valid_email(email: str) -> None:
    if is_include_emoji(email):
        raise EmailErrorException()

    try:
        validate_email(email)
    except EmailNotValidError:
        raise EmailErrorException()

    if email_blacklist_service.is_in_blacklist(email):
        raise EmailErrorException()


def assert_if_not_valid_emails(emails: List[str]) -> None:
    for email in emails:
        assert_if_not_valid_email(email)


def send(from_email: Email, to_emails: List[str], subject, text=None, html=None) -> bool:
    try:
        MailgunHelper.send(from_email, to_emails, subject, text, html)
    except EmailSendErrorException:
        sentry.exception()

        try:
            MandrillHelper.send(from_email, to_emails, subject, text, html)
        except EmailSendErrorException:
            sentry.exception()
            return False

    return True
