from django.conf import settings


class GeneralConfig:
    @staticmethod
    def is_dev() -> bool:
        return settings.DEBUG

    @staticmethod
    def get_environment() -> str:
        return settings.ENVIRONMENT

    @staticmethod
    def get_version() -> str:
        return settings.VERSION

    @staticmethod
    def get_site_domain() -> str:
        return settings.SITE_DOMAIN

    @staticmethod
    def get_store_url() -> str:
        return settings.STORE_URL

    @staticmethod
    def get_ridibooks_login_url() -> str:
        return settings.RIDIBOOKS_LOGIN_URL


class FilterConfig:
    @staticmethod
    def ignore_404_filter_url() -> list:
        return settings.IGNORE_404_FILTER_URLS
