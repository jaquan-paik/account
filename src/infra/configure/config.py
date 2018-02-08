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
    def get_site() -> str:
        return settings.SITE

    @staticmethod
    def is_enforce_2fa() -> bool:
        return settings.ENFORCE_TWO_FACTOR_AUTH


class FilterConfig:
    @staticmethod
    def ignore_404_filter_url() -> list:
        return settings.IGNORE_404_FILTER_URLS
