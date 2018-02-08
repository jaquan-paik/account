from django.conf import settings

from infra.email.dto import Email


class AnalysisSlowQueryConfig:
    @staticmethod
    def get_analysis_db_list():
        return settings.ANALYSIS_SLOW_QUERY_DB_LIST

    @staticmethod
    def get_analysis_from_mail() -> Email:
        return Email(settings.ANALYSIS_SLOW_QUERY_FROM_EMAIL)

    @staticmethod
    def get_analysis_to_mails():
        return settings.ANALYSIS_SLOW_QUERY_TO_EMAILS
