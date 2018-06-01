from typing import Dict, List

from django.db import connections


#  https://github.com/pbs/django-heartbeat
#  https://github.com/pbs/django-heartbeat/blob/master/src/heartbeat/checkers/databases.py
class CheckDatabase:
    @classmethod
    def check(cls) -> List:
        databases_info = []
        for db in connections:
            databases_info.append(cls._get_connection_info(connections[db]))

        return databases_info

    @classmethod
    def _get_connection_info(cls, connection) -> Dict:
        engine = connection.settings_dict.get('ENGINE')

        return {
            'alias': connection.alias,
            'name': connection.settings_dict.get('NAME'),
            'engine': engine,
            'version': cls._get_database_version(connection, engine),
            'host': connection.settings_dict.get('HOST'),
            'port': connection.settings_dict.get('PORT'),
        }

    @classmethod
    def _get_database_version(cls, connection, engine):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.dummy':
            return None

        engines = {
            'django.db.backends.postgresql': 'SELECT version();',
            'django.db.backends.postgresql_psycopg2': 'SELECT version();',
            'django.db.backends.mysql': 'SELECT version();',
            'django.db.backends.sqlite3': 'select sqlite_version();',
            'django.db.backends.oracle': 'select * from v$version;',
            'django.contrib.gis.db.backends.mysql': 'SELECT version();',
            'django.contrib.gis.db.backends.postgis': 'SELECT version();',
            'django.contrib.gis.db.backends.spatialite': (
                'select sqlite_version();'
            ),
            'django.contrib.gis.db.backends.oracle': 'select * from v$version;',
        }
        query = engines[engine]
        return cls._execute_sql(connection, query)

    @classmethod
    def _execute_sql(cls, connection, query):
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result
