import jsonpickle
from django.core.exceptions import ObjectDoesNotExist


class RedisDocument:
    objects = None

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

        if hasattr(self, 'reg_date') and getattr(self, 'reg_date') is None:
            from datetime import datetime

            now = datetime.now()
            self.created = now
            self.last_modified = now

    @staticmethod
    def serialize(doc_obj):
        if not isinstance(doc_obj, RedisDocument):
            raise ValueError('doc_obj is not a instance of RedisDocument')

        return jsonpickle.encode(doc_obj)

    @staticmethod
    def unserialize(serialized):
        if not serialized:
            raise ObjectDoesNotExist()

        return jsonpickle.decode(serialized)

    def save(self) -> None:
        self.objects.save(self)
