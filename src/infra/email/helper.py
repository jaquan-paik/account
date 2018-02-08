import hashlib
import hmac

import mandrill
import requests

from .config import MailConfig
from .dto import Email
from .exceptions import EmailSendErrorException


class MandrillHelper:
    @staticmethod
    def send(from_email: Email, to_email, subject: str, text: str=None, html: str=None) -> None:
        mandrill_client = mandrill.Mandrill(MailConfig.get_mandrill_api_key())
        to_email = [{'email': email} for email in to_email]
        message = {
            'from_email': from_email.email,
            'to': to_email,
            'html': html,
            'subject': subject,
            'text': text,
        }

        if from_email.has_name():
            message['from_name'] = from_email.name

        results = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
        for result in results:
            if result['status'] != 'sent':
                raise EmailSendErrorException('mandrill send error')


class MailgunHelper:
    @staticmethod
    def send(from_email: Email, to_email, subject: str, text: str=None, html: str=None) -> None:
        resp = requests.post(
            MailConfig.get_mailgun_message_url(),
            auth=('api', MailConfig.get_mailgun_api_auth()),
            data={
                'from': str(from_email),
                'to': to_email,
                'subject': subject,
                'text': text,
                'html': html,
            }
        )

        status_code = resp.status_code
        if status_code != 200:
            raise EmailSendErrorException('mailgun send error')

    @staticmethod
    def is_valid_webhook_token(timestamp: int, token: str, signature: str) -> None:
        hmac_digest = hmac.new(
            key=str.encode(MailConfig.get_mailgun_api_auth()),
            msg=str.encode('{}{}'.format(timestamp, token)),
            digestmod=hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, hmac_digest)
