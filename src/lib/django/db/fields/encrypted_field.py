from django.db import models

from lib.crypto.encrypt import CryptoHelper


class EncryptedFieldMixin:
    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key', None)
        self.crypto = CryptoHelper(self.key)

        super().__init__()

    def from_db_value(self, value, expression, connection, context):
        if value is None or len(value) <= 1:
            return value

        try:
            return self.crypto.decrypt(value)
        except ValueError:
            return value

    def get_prep_value(self, value):
        if value is None or value == '':
            return value

        return self.crypto.encrypt(value)


class EncryptedCharField(EncryptedFieldMixin, models.CharField):
    pass


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    pass
