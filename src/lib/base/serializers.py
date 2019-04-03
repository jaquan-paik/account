from typing import Dict, List

from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class KSTDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        result = super().to_representation(value)
        return result + '+09:00'


class BaseSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BaseModelSerializer(ModelSerializer):
    pass


BaseModelSerializer.serializer_field_mapping[models.DateTimeField] = KSTDateTimeField


class DynamicChildFieldsSerializer(BaseSerializer):
    def __init__(self, *args, fields: Dict[str, List[str]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._allowed_fields = fields

    def to_representation(self, instance):
        if self._allowed_fields:
            for field, allowed_fields in self._allowed_fields.items():
                allowed = set(allowed_fields)
                existing = set(self.fields[field].child.fields.keys())
                for field_name in existing - allowed:
                    self.fields[field].child.fields.pop(field_name)

        return super().to_representation(instance)
