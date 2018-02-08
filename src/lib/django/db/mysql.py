from django.db.backends.mysql.features import DatabaseFeatures
from django.utils.functional import cached_property


class MysqlDatabaseFeatures(DatabaseFeatures):
    @cached_property
    def supports_microsecond_precision(self):
        return False
