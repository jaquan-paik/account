from infra.configure.config import GeneralConfig
from infra.configure.constants import SiteType
from infra.storage.database.constants import Database


class DbRouter:
    def db_for_read(self, model, **hints):
        if GeneralConfig.get_site() == SiteType.TEST:
            return Database.DEFAULT
        return Database.READ

    def db_for_write(self, model, **hints):
        if GeneralConfig.get_site() == SiteType.TEST:
            return Database.DEFAULT
        return Database.WRITE
