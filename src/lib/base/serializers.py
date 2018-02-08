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
