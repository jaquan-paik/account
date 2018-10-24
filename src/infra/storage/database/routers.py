from django.conf import settings

from infra.storage.database.constants import Database


class DbRouter:
    def db_for_read(self, model, **hints):
        return Database.DEFAULT

    def db_for_write(self, model, **hints):
        return Database.DEFAULT

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)  # pylint: disable=protected-access
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)  # pylint: disable=protected-access
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            return False
        return None  # pylint: simplifiable-if-statement
