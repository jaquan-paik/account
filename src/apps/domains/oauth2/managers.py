from datetime import datetime

from django.db import connection
from django.db.models import Manager

from infra.storage.database.constants import Database
from lib.django.db.caching.managers import BaseCachingManager


class ApplicationManager(Manager):
    pass


class RefreshTokenManager(Manager):
    def revoke_by_expire_date(self, expire_date: datetime, limit):
        table_name = self.model._meta.db_table  # pylint:disable=protected-access
        with connection.cursor() as c:
            c.execute(f'DELETE FROM {table_name} WHERE expires < "{expire_date}" LIMIT {limit}')


class GrantManager(Manager):
    def revoke_by_expire_date(self, expire_date: datetime, limit):
        table_name = self.model._meta.db_table  # pylint:disable=protected-access
        with connection.cursor() as c:
            c.execute(f'DELETE FROM {table_name} WHERE expires < "{expire_date}" LIMIT {limit}')
