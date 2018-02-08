from django.apps import AppConfig


class DjangoAppConfig(AppConfig):
    name = 'lib.django'
    label = 'lib_django_app'
    verbose_name = 'Django custom'

    def ready(self):
        # mysql database
        # don't use supports_microsecond_precision
        from django.db.backends.mysql.base import DatabaseWrapper
        from lib.django.db.mysql import MysqlDatabaseFeatures
        DatabaseWrapper.features_class = MysqlDatabaseFeatures

        # DRF model serializer
        # Force KST
        from django.db import models
        from rest_framework.serializers import ModelSerializer
        from lib.base.serializers import KSTDateTimeField
        ModelSerializer.serializer_field_mapping[models.DateTimeField] = KSTDateTimeField
