from typing import List

DEFAULT_LIMIT = 1000


class BaseRepository:
    model_class = None

    @classmethod
    def create(cls, entities: List, is_bulk: bool = False, bulk_bundle_count: int = 1000):
        if is_bulk:
            # bulk 로 하게 되면 pk 가 나오지 않기 때문에 유의한다.
            cls.model_class.objects.bulk_create(entities, batch_size=bulk_bundle_count)

        else:
            for entity in entities:
                entity.save(force_insert=True)

        return entities

    @staticmethod
    def update(entities: List, update_fields: List = None):
        for entity in entities:
            entity.save(update_fields=update_fields)

    @classmethod
    def delete(cls, entities: List):
        for entity in entities:
            entity.delete()

    @classmethod
    def soft_delete(cls, entities: List):
        for entity in entities:
            entity.is_deleted = True
            entity.save(update_fields=['is_deleted', ])

    @classmethod
    def find(cls, offset: int = 0, limit: int = DEFAULT_LIMIT) -> List:
        return cls.model_class.objects.all()[offset:offset + limit]

    @classmethod
    def find_all(cls) -> List:
        return cls.model_class.objects.all()

    @classmethod
    def find_by_ids(cls, ids: List) -> List:
        return cls.model_class.objects.filter(id__in=ids)

    @classmethod
    def get_by_id(cls, model_id: int):
        return cls.model_class.objects.get(id=model_id)
