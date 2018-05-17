from django.db import models
from django.db.backends.mysql.features import DatabaseFeatures
from django.utils.functional import cached_property

MYSQL_ENGINE = 'django.db.backends.mysql'


class MysqlDatabaseFeatures(DatabaseFeatures):
    @cached_property
    def supports_microsecond_precision(self):
        return False


class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == MYSQL_ENGINE:
            return "tinyint"
        return super(TinyIntegerField, self).db_type(connection)


class TinyBooleanField(models.BooleanField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == MYSQL_ENGINE:
            return "tinyint"
        return super(TinyBooleanField, self).db_type(connection)


class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == MYSQL_ENGINE:
            return "tinyint unsigned"
        return super(PositiveTinyIntegerField, self).db_type(connection)
