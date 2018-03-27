from datetime import datetime

from django.db import connection
from django.db.models import Manager


class RefreshTokenManager(Manager):
    def revoke_by_expire_date(self, expire_date: datetime, limit):
        table_name = self.model._meta.db_table
        with connection.cursor() as c:
            c.execute(f'DELETE FROM {table_name} WHERE expires < "{expire_date}" LIMIT {limit}')


class GrantManager(Manager):
    def revoke_by_expire_date(self, expire_date: datetime, limit):
        table_name = self.model._meta.db_table
        with connection.cursor() as c:
            c.execute(f'DELETE FROM {table_name} WHERE expires < "{expire_date}" LIMIT {limit}')
