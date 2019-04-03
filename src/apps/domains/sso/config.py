from django.conf import settings


class SSOConfig:
    @staticmethod
    def get_sso_redirect_domain() -> str:
        return settings.SSO_REDIRECT_DOMAIN

    @staticmethod
    def get_sso_login_url() -> str:
        return settings.SSO_LOGIN_URL

    @staticmethod
    def get_sso_otp_key() -> str:
        return settings.SSO_OTP_KEY
