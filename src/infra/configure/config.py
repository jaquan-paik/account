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


class FilterConfig:
    @staticmethod
    def ignore_404_filter_url() -> list:
        return settings.IGNORE_404_FILTER_URLS
