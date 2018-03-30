from datetime import datetime

from django.db import connection
from django.db.models import Manager

from apps.domains.oauth2.constants import REFRESH_TOKEN_CACHE_TTL, APPLICATION_CACHE_TTL
from infra.storage.database.constants import Database
from lib.django.db.caching.managers import BaseCachingManager


class ApplicationManager(BaseCachingManager):
    CACHE_TTL = APPLICATION_CACHE_TTL
    MASTER_DATABASE = Database.WRITE


class RefreshTokenManager(BaseCachingManager):
    CACHE_TTL = REFRESH_TOKEN_CACHE_TTL
    MASTER_DATABASE = Database.WRITE

    def revoke_by_expire_date(self, expire_date: datetime, limit):
        table_name = self.model._meta.db_table  # pylint:disable=protected-access
        with connection.cursor() as c:
            c.execute(f'DELETE FROM {table_name} WHERE expires < "{expire_date}" LIMIT {limit}')


class GrantManager(Manager):
    def revoke_by_expire_date(self, expire_date: datetime, limit):
        table_name = self.model._meta.db_table  # pylint:disable=protected-access
        with connection.cursor() as c:
            c.execute(f'DELETE FROM {table_name} WHERE expires < "{expire_date}" LIMIT {limit}')
