from django.conf import settings


class MailConfig:
    @staticmethod
    def get_mailgun_message_url() -> str:
        return settings.MAILGUN_MESSAGE_URL

    @staticmethod
    def get_mailgun_api_auth() -> str:
        return settings.MAILGUN_API_AUTH

    @staticmethod
    def get_mandrill_api_key() -> str:
        return settings.MANDRILL_API_KEY
